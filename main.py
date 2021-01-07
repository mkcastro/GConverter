# %%
import datetime
import os

import pandas as pd
import pikepdf
import tabula


# %%
def get_latest_file_unencrypted_file():
    encrypted = get_latest_file("./encrypted/")
    unencrypted = get_latest_file("./unencrypted/")
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)
    extension = ".csv"
    unencrypted_filename = current_date_and_time_string + extension

    if encrypted == unencrypted:
        decrypt(encrypted, "password", unencrypted_filename)

    return unencrypted_filename


def get_latest_file(directory):
    return os.listdir()


def decrypt(input_filename, password, output_filename):
    pdf = pikepdf.open(input_filename, password=password)
    pdf.save(output_filename)


def convert_pdf_to_csv(filename):
    output_filename = filename[:3]
    tabula.convert_into(
        filename, output_filename + "csv", output_format="csv", pages="all"
    )


def cleanup_headers_and_footers(df):
    starting_balance_filter = df["description"] == "STARTING BALANCE"
    ending_balance_filter = df["description"] == "ENDING BALANCE"
    total_debit_filter = df["description"] == "Total Debit"
    df.drop(index=df[starting_balance_filter].index, inplace=True)
    df.drop(index=df[ending_balance_filter].index, inplace=True)
    df.drop(index=df[total_debit_filter].index, inplace=True)


def merge_multiline_transactions(df):
    pass


def merge_page_breaks(df):
    pass


def rename_columns(df):
    df.rename(
        columns={"Date and Time": "datetime", "Reference No.": "reference_no"},
        inplace=True,
    )
    df.columns = [x.lower() for x in df.columns]


# %%
def main():
    convert_pdf_to_csv("./unencrypted/1.pdf")
    df = pd.read_csv("./output/1.csv", dtype={"Reference No.": object})
    rename_columns(df)
    cleanup_headers_and_footers(df)
    merge_multiline_transactions(df)
    merge_page_breaks(df)
    print(df)


if __name__ == "__main__":
    main()
