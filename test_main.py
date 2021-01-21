import unittest

import pandas as pd


def merge(df):
    index = 0
    prefix = str(df.loc[index]["description"])
    suffix = str(df.loc[index + 2]["description"])

    df.at[index + 1, "description"] = prefix + " " + suffix

    df.drop(index=index, inplace=True)
    df.drop(index=index + 2, inplace=True)

    df.reset_index(inplace=True)


class TestMain(unittest.TestCase):
    def test_get_row_type(self):
        left = pd.DataFrame(
            {
                "datetime": ["2018-08-27 05:12 PM"],
                "description": ["Send Money from 09975187259 gcash_atm2"],
                "reference_no": ["0002108470539"],
                "debit": ["3000.00"],
                "credit": [""],
                "balance": ["2539.25"],
            }
        )
        right = pd.DataFrame(
            {
                "datetime": ["", "2018-08-27 05:12 PM", ""],
                "description": [
                    "Send Money from 09975187259",
                    "",
                    "gcash_atm2",
                ],  # flake8: noqa
                "reference_no": ["", "0002108470539", ""],
                "debit": ["", "3000.00", ""],
                "credit": ["", "", ""],
                "balance": ["", "2539.25", ""],
            }
        )

        merge(right)

        # pd.testing.assert_frame_equal(left, right)
        pd.testing.assert_series_equal(left["datetime"], right["datetime"])
        pd.testing.assert_series_equal(
            left["description"], right["description"]
        )  # flake8: noqa
        pd.testing.assert_series_equal(
            left["reference_no"], right["reference_no"]
        )  # flake8: noqa
        pd.testing.assert_series_equal(left["debit"], right["debit"])
        pd.testing.assert_series_equal(left["credit"], right["credit"])
        pd.testing.assert_series_equal(left["balance"], right["balance"])
