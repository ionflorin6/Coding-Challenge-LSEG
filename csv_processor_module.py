import csv
import random
import statistics
from dateutil.parser import parse as parse_date

# Check if a string is a date - in any format.
def is_date(string, fuzzy=False):
    try:
        parse_date(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


# Class used for processing input csv files.
class CSV_processor:
    def __init__(self, file_path, output_dir, file_name, consecutive_data_points):
        self.consecutive_data_points = consecutive_data_points
        self.output_path = output_dir + "/out_" + file_name
        self.output_dir = output_dir
        self.file_name = file_name
        self.file_path = file_path
        self.stock_price_mean = 0
        self.number_of_rows = 0

    # Validate csv format and structure.
    def init_csv_processor(self):
        if not self.file_path.endswith('.csv'):
            print(f"File [{self.file_path}] is not csv file.\n")
            return -1

        try:
            with open(self.file_path, 'r') as csv_file:
                content = csv.reader(csv_file)
                sum = 0
                number_of_rows = 0
                price = 0

                for row in content:
                    # Check if there are 3 columns in the input csv (stock-id, timestamp, stock price value).
                    if len(row) != 3:
                        print(f"In file [{self.file_path}], csv file format is incorrect.\n")
                        return -1

                    # Check if the second column is a date.
                    if not is_date(row[1]):
                        print(f"In file [{self.file_path}], csv file date format is incorrect [{row[1]}].\n")
                        return -1

                    number_of_rows += 1

                    # Check the stock price value can be converted to a number.
                    try:
                        price = float(row[2])
                    except ValueError:
                        print(f"In file [{self.file_path}], csv file stock price format is incorrect.\n"
                              f"Could not convert stock price to float [{price}].\n")
                        return -1

                    sum += price

                # Check if csv file is empty by number of rows.
                if number_of_rows == 0:
                    print(f"Csv file [{self.file_path}] is empty.\n")
                    return -1

                self.stock_price_mean = sum/number_of_rows
                self.number_of_rows = number_of_rows

        except FileNotFoundError:
            print(f"File [{self.file_path}] not found.\n")
            return -1

        # Return the error type and message string in case it is not a FileNotFoundError.
        except OSError as e:
            print(f"File [{self.file_path}] error({e.errno}): {e.strerror}.\n")
            return -1

        else:
            return 0

    # Return exactly 30 consecutive data points starting from a random timestamp within the file.
    def get_random_data_points(self):
        with open(self.file_path, 'r') as csv_file:
            content = csv.reader(csv_file)
            random_data_point = random.randint(0, self.number_of_rows - self.consecutive_data_points - 1)
            output_list = []

            # Save the 30 consecutive data points into a list.
            for i, line in enumerate(content):
                if i == random_data_point:
                    for _ in range(0, self.consecutive_data_points):
                        output_list.append(next(content))
                    break
            return output_list

    # Convert the stock price values from strings to float.
    def get_clean_data_points(self, data_points_list):
        clean_data_points = []

        for data_point in data_points_list:
            clean_data_points.append(float(data_point[2]))
        return clean_data_points

    def get_outliers(self, data_points_list):
        clean_data_points_list = self.get_clean_data_points(data_points_list)

        # Determine the thresholds that define the outliers.
        data_mean = statistics.mean(clean_data_points_list)
        standard_deviation = statistics.stdev(clean_data_points_list)
        min_threshold = data_mean - (2 * standard_deviation)
        max_threshold = data_mean + (2 * standard_deviation)

        # Build the headers for the output csv files.
        outliers_list = [['Stock-ID', 'Timestamp', 'actual stock price at that timestamp', 'mean of 30 data points',
                         'actual stock price – mean', '% deviation over and above the threshold']]

        for row in data_points_list:
            if float(row[2]) < min_threshold or float(row[2]) > max_threshold:
                row.append(data_mean)
                row.append(self.stock_price_mean)
                row.append(abs((data_mean - float(row[2])) / 100))
                outliers_list.append(row)

        # Write the final output with the outliers in a csv file.
        with open(self.output_path, 'w', newline='') as outliers_csv:
            outliers_content = csv.writer(outliers_csv)
            outliers_content.writerows(outliers_list)