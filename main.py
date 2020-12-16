# %%
import datetime
import os

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


def convert_pdf(filename):
    return tabula.read_pdf(filename, pages="1-10")


def convert_dataframe_to_workable_data():
    pass


def merge_page_breaks():
    pass


def display():
    pass


def main():
    filename = get_latest_file_unencrypted_file()
    filename
    # dataframe = convert_pdf(filename)
    # convert_dataframe_to_workable_data()
    # merge_page_breaks()
    # display()


if __name__ == "__main__":
    main()
