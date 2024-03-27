import csv_processor_module
import os
import sys
import argparse

consecutive_data_points = 30
ROOT_DIR = "./stock_price_data_files"

parser = argparse.ArgumentParser()

parser.add_argument("-fn", "--files-number", default="1", dest="filesnumber", help="Number of files to be sampled for each Stock Exchange")
parser.add_argument("-i", "--input-directory", default="./stock_price_data_files", dest="inputdirectory", help="Root directory for stock exchanges")
parser.add_argument("-o", "--output-directory", default="./output", dest="outputdirectory", help="Output directory for csv files")

args = parser.parse_args()

def stock_exchange_parser(files_number, input_directory, output_directory):
    if files_number < 0:
        print(f"Invalid file number [{files_number}].")
        sys.exit()

    stock_exchanges = os.listdir(input_directory)

    if len(stock_exchanges) == 0:
        print(f"No stock exchanges in input directory [{input_directory}].")
        sys.exit()

    for stock_exchange in stock_exchanges:
        stock_exchange_path = input_directory + "/" + stock_exchange

        if not os.path.isdir(stock_exchange_path):
            print(f"Skipping [{stock_exchange_path}] as it is not a directory.")
            continue

        csv_files = os.listdir(stock_exchange_path)
        if len(csv_files) == 0:
            print(f"No csv files present in [{(stock_exchange_path)}]"
                  f"\nContinuing with the rest of the stock exchanges.")
            continue

        if files_number > len(csv_files):
            print(f"File number [{files_number}] is greater than number of csv files [{len(csv_files)}] for"
                  f"stock exchange [{stock_exchange}]."
                  f"\nContinuing with [{len(csv_files)}] files.")

        for csv_file_index in range(0, min(files_number, len(csv_files))):
            file_path = stock_exchange_path + "/" + csv_files[csv_file_index]
            csv_processor = csv_processor_module.CSV_processor(file_path, output_directory, csv_files[csv_file_index],
                                                               consecutive_data_points)

            if csv_processor.init_csv_processor() != 0:
                continue
            random_data_set_rows = csv_processor.get_random_data_points()
            csv_processor.get_outliers(random_data_set_rows)


if __name__ == "__main__":
    if not os.path.isdir(args.inputdirectory):
        print(f"Input directory [{args.inputdirectory}] doesn't exist.")
        sys.exit()

    if not os.path.isdir(args.outputdirectory):
        print(f"Output directory [{args.outputdirectory}] doesn't exist.")
        sys.exit()

    stock_exchange_parser(int(args.filesnumber), args.inputdirectory, args.outputdirectory)