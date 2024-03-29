import csv_processor_module
import os
import sys
import argparse

CONSECUTIVE_DATA_POINTS = 30

# Define arguments for the script - files number, input and output directories
parser = argparse.ArgumentParser()

parser.add_argument("-fn", "--files-number", type=int, default="1", dest="filesnumber", help="Number of files to be sampled for each Stock Exchange")
parser.add_argument("-i", "--input-directory", default="./stock_price_data_files", dest="inputdirectory", help="Root directory for stock exchanges")
parser.add_argument("-o", "--output-directory", default="./output", dest="outputdirectory", help="Output directory for csv files")

args = parser.parse_args()


def stock_exchange_parser(files_number, input_directory, output_directory):
    # Check if the number of files given is an integer.
    try:
        int(files_number)
    except ValueError:
        print(f"Invalid file number inserted [{files_number}].\n"
              f"File number must be integer.\n")
        sys.exit()

    # Accept only positive numbers.
    if files_number < 0:
        print(f"Invalid file number [{files_number}].\n")
        sys.exit()

    # Collect the contents of the input directory.
    stock_exchanges = os.listdir(input_directory)

    # Check if the input directory is empty.
    if len(stock_exchanges) == 0:
        print(f"No stock exchanges in input directory [{input_directory}].\n")
        sys.exit()

    for stock_exchange in stock_exchanges:
        stock_exchange_path = input_directory + "/" + stock_exchange

        # Validate if the content parsed is a directory.
        if not os.path.isdir(stock_exchange_path):
            print(f"Skipping [{stock_exchange_path}] as it is not a directory.\n")
            continue

        csv_files = os.listdir(stock_exchange_path)
        if len(csv_files) == 0:
            print(f"No csv files present in [{stock_exchange_path}].\n"
                  f"Continuing with the rest of the stock exchanges.\n")
            continue

        # Address the possibility of having less csv files than the files number given as input.
        if files_number > len(csv_files):
            print(f"File number [{files_number}] is greater than number of csv files [{len(csv_files)}] for "
                  f"stock exchange [{stock_exchange}].\n"
                  f"Continuing with [{len(csv_files)}] files.\n")

        # Keep processing the csv files that are present in the directories.
        for csv_file_index in range(0, min(files_number, len(csv_files))):
            file_path = stock_exchange_path + "/" + csv_files[csv_file_index]
            csv_processor = csv_processor_module.CSV_processor(file_path, output_directory, csv_files[csv_file_index],
                                                               CONSECUTIVE_DATA_POINTS)

            # Check if the validation of the csv file passed.
            if csv_processor.init_csv_processor() != 0:
                continue
            random_data_set_rows = csv_processor.get_random_data_points()
            csv_processor.get_outliers(random_data_set_rows)


if __name__ == "__main__":
    # Check if the input and output directories exist.
    if not os.path.isdir(args.inputdirectory):
        print(f"Input directory [{args.inputdirectory}] doesn't exist.\n")
        sys.exit()

    if not os.path.isdir(args.outputdirectory):
        print(f"Output directory [{args.outputdirectory}] doesn't exist.\n")
        sys.exit()

    stock_exchange_parser(args.filesnumber, args.inputdirectory, args.outputdirectory)