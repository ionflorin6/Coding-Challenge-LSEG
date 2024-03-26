import csv_processor_module
import os

cosecutive_data_points = 30
ROOT_DIR = "./stock_price_data_files"

def stock_exchange_parser(files_number):
    stock_exchanges = os.listdir(ROOT_DIR)
    for stock_exchange in stock_exchanges:
        csv_files = os.listdir(ROOT_DIR + "/" + stock_exchange)
        if len(csv_files) != 0:
            if files_number > len(csv_files):
                print("Files_number bigger than existing csv files")
            for csv_file_index in range(0, min(files_number, len(csv_files))):
                file_path = ROOT_DIR + "/" + stock_exchange + "/" + csv_files[csv_file_index]
                csv_processor = csv_processor_module.CSV_processor(file_path, csv_files[csv_file_index],
                                                                   cosecutive_data_points)
                random_data_set_rows = csv_processor.get_random_data_points()
                csv_processor.get_outliers(random_data_set_rows)
        else:
            print("No csv files present")

stock_exchange_parser(2)