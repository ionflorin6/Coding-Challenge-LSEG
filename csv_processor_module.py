import csv
import random
import statistics
from dateutil.parser import parse as parse_date


def is_date(string, fuzzy=False):
    try:
        parse_date(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


class CSV_processor:
    def __init__(self, file_path, output_dir, file_name, consecutive_data_points):
        self.consecutive_data_points = consecutive_data_points
        self.output_path = output_dir + "/out_" + file_name
        self.output_dir = output_dir
        self.file_name = file_name
        self.file_path = file_path
        self.stock_price_mean = 0
        self.number_of_rows = 0

    def init_csv_processor(self):
        if not self.file_path.endswith('.csv'):
            print(f"File [{self.file_path}] is not csv file.")
            return -1

        try:
            with open(self.file_path, 'r') as csv_file:
                content = csv.reader(csv_file)
                sum = 0
                number_of_rows = 0
                price = 0

                for row in content:
                    if len(row) != 3:
                        print(f"In file [{self.file_path}], csv file format is incorrect.")
                        return -1

                    if not is_date(row[1]):
                        print(f"In file [{self.file_path}], csv file date format is incorrect [{row[1]}].")
                        return -1

                    number_of_rows += 1
                    try:
                        price = float(row[2])
                    except ValueError:
                        print(f"In file [{self.file_path}], csv file stock price format is incorrect."
                              f"\nCould not convert stock price to float [{price}].")
                        return -1

                    sum += price
                if number_of_rows == 0:
                    print(f"Csv file [{self.file_path}] is empty.")
                    return -1

                self.stock_price_mean = sum/number_of_rows
                self.number_of_rows = number_of_rows
        except FileNotFoundError:
            print(f"File [{self.file_path}] not found.")
            return -1

        except OSError as e:
            print(f"File [{self.file_path}] error({e.errno}): {e.strerror}")
            return -1

        else:
            return 0

    def get_random_data_points(self):
        with open(self.file_path, 'r') as csv_file:
            content = csv.reader(csv_file)
            random_data_point = random.randint(0, self.number_of_rows - self.consecutive_data_points - 1)
            output_list = []

            for i, line in enumerate(content):
                if i == random_data_point:
                    for _ in range(0, self.consecutive_data_points):
                        output_list.append(next(content))
                    break
            return output_list
    
    def get_clean_data_points(self, data_points_list):
        clean_data_points = []

        for data_point in data_points_list:
            clean_data_points.append(float(data_point[2]))
        return clean_data_points

    def get_outliers(self, data_points_list):
        clean_data_points_list = self.get_clean_data_points(data_points_list)
        data_mean = statistics.mean(clean_data_points_list)
        standard_deviation = statistics.stdev(clean_data_points_list)
        min_threshold = data_mean - (2 * standard_deviation)
        max_threshold = data_mean + (2 * standard_deviation)
        outliers_list = [['Stock-ID', 'Timestamp', 'actual stock price at that timestamp', 'mean of 30 data points',
                         'actual stock price – mean', '% deviation over and above the threshold']]

        for row in data_points_list:
            if float(row[2]) < min_threshold or float(row[2]) > max_threshold:
                row.append(data_mean)
                row.append(self.stock_price_mean)
                row.append(abs((data_mean - float(row[2])) / 100))
                outliers_list.append(row)

        with open(self.output_path, 'w', newline='') as outliers_csv:
            outliers_content = csv.writer(outliers_csv)
            outliers_content.writerows(outliers_list)