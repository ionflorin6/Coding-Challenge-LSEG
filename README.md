# Coding-Challenge-LSEG

## Description

This code is designed to process csv files that contain stock IDs, timestamps and stock price values for different global "Exchanges".

## Requirements

In order to run the code from this project, you will need pip and python installed on your machine.

## Setup

Clone the git project into your desired path.

```# for the SSH option, use:
git@github.com:ionflorin6/Coding-Challenge-LSEG.git
```

Open your terminal or command prompt into the project's folder and install the packages needed to run the code.

```
# make sure you have pip installed
pip install -r requirements.txt
```

## Usage

From the project's folder, in the terminal or command prompt, run the script with the appropriate options:\


usage: python .\main.py [-h] [-fn FILESNUMBER] [-i INPUTDIRECTORY] [-o OUTPUTDIRECTORY]

options:
  -h, --help            show this help message and exit\
  -fn FILESNUMBER, --files-number FILESNUMBER\
                        Number of files to be sampled for each Stock Exchange\
                        Default value = 1\
  -i INPUTDIRECTORY, --input-directory INPUTDIRECTORY\
                        Root directory for stock exchanges\
                        Default value = "./stock_price_data_files"\
  -o OUTPUTDIRECTORY, --output-directory OUTPUTDIRECTORY\
                        Output directory for csv files\
                        Default value = "./output"\


```
# for example:
python .\main.py -fn 2 -i "./stock_price_data_files" -o "."
```

After the script execution, the output csv files can be found in the output directory. They can be identified by the beginning characters "out_".\
An output csv file containing outliers will be generated for each input csv.
