# %%
import datetime
import os

import pandas as pd
import pikepdf
import tabula

from settings import PASSWORD


# %%
def get_latest_file_unencrypted_file():
    encrypted = get_latest_file("./encrypted/")
    unencrypted = get_latest_file("./unencrypted/")
    current_date_and_time = datetime.datetime.now()
    current_date_and_time_string = str(current_date_and_time)
    extension = ".csv"
    unencrypted_filename = current_date_and_time_string + extension

    if encrypted == unencrypted:
        decrypt_pdf(encrypted, "password", unencrypted_filename)

    return unencrypted_filename


def get_latest_file(directory):
    return os.listdir()


def convert_pdf_to_csv(filename):
    output_filename = filename[:-3]
    output_filename = output_filename.replace("./unencrypted", "./output")
    tabula.convert_into(
        filename, output_filename + "csv", output_format="csv", pages="all"
    )


def cleanup_headers_and_footers(df):
    starting_balance_filter = df["description"] == "STARTING BALANCE"
    ending_balance_filter = df["description"] == "ENDING BALANCE"
    total_debit_filter = df["description"] == "Total Debit"
    total_credit_filter = df["description"] == "Total Credit"
    df.drop(index=df[starting_balance_filter].index, inplace=True)
    df.drop(index=df[ending_balance_filter].index, inplace=True)
    df.drop(index=df[total_debit_filter].index, inplace=True)
    df.drop(index=df[total_credit_filter].index, inplace=True)


def merge_page_breaks(df):
    pass


def rename_columns(df):
    df.rename(
        columns={"Date and Time": "datetime", "Reference No.": "reference_no"},
        inplace=True,
    )
    df.columns = [x.lower() for x in df.columns]


def decrypt_pdf(input_filename, output_filename):
    pdf = pikepdf.open(input_filename, password=PASSWORD)
    pdf.save(output_filename)


# %%
def main():
    decrypt_pdf("./encrypted/1.pdf", "./unencrypted/1.pdf")
    convert_pdf_to_csv("./unencrypted/1.pdf")
    df = pd.read_csv("./output/1.csv", dtype={"Reference No.": object})
    rename_columns(df)
    cleanup_headers_and_footers(df)
    merge_multiline_transactions(df)
    merge_page_breaks(df)
    # df.set_index('datetime', inplace=True)
    print(df)


if __name__ == "__main__":
    # main()
    pass

# %%
df = pd.read_csv("./output/1.csv", dtype={"Reference No.": object})
df
# %%
rename_columns(df)
df
# %%
cleanup_headers_and_footers(df)
df
# %%
# TODO: i stopped here


def merge_multiline_transactions(df):
    for index, row in df.iterrows():
        datetime = row["datetime"]

        if pd.isnull(datetime) or (type(datetime) == list):
            try:
                # todo: check what column is overflowing,
                # if it's either description or reference_no
                prefix = df.loc[index]["description"]
                suffix = df.loc[index + 2]["description"]

                df.at[index + 1, "description"] = prefix + " " + suffix

                df.drop(index=index, inplace=True)
                df.drop(index=index + 2, inplace=True)

                print(index, "not cool")
            except KeyError:
                pass
        else:
            # print(index)
            pass


merge_multiline_transactions(df)
df
# %%
merge_page_breaks(df)
df
# %%
print(df)
