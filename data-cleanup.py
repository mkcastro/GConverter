# %%
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# %%
pd.set_option("display.max_colwidth", None)


# %%
# pd.set_option('display.max_rows', None)


# %%
df = pd.read_csv("./output/2.csv", dtype={"reference_no": object})
df


# %%
def datetime_merged(row):
    pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M$"
    if re.search(pattern, str(row["datetime"])):
        return False
    return True


# %%
def value_is_nan(value):
    if pd.isnull(value) or (type(value) == list):
        return True
    return False


# %%
def split_datetime(df):
    for index, row in df.iterrows():

        pattern = r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M)\s(.*)"
        match = re.search(pattern, str(row["datetime"]))
        is_nan = value_is_nan(row["datetime"])

        if datetime_merged(row) and not is_nan and match:
            correct_datetime = match[1]
            correct_description = match[2]

            df.at[index, "reference_no"] = row["description"]
            df.at[index, "description"] = correct_description
            df.at[index, "datetime"] = correct_datetime

        if datetime_merged(row) and not value_is_nan(row["datetime"]):
            df.at[index, "description"] = row["datetime"]
            df.at[index, "datetime"] = np.NaN


# %%
pattern = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M$"
merged_datetime_df = df[~df["datetime"].str.contains(pattern, na=False)]
merged_datetime_df


# %%
split_datetime(df)
df


# %%
# split rows with combined description
merged_description_filter = df["description"].str.contains(
    r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M", na=False
)
df[merged_description_filter]


# %%
def description_merged(row):
    pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M"
    if re.search(pattern, str(row["description"])):
        return True
    return False


# %%
def split_description(df):
    for index, row in df.iterrows():

        pattern = r"(.*)(\d{4}-\d{2}-\d{2} \d{2}:\d{2} (?:A|P)M)\s(.*)"
        match = re.search(pattern, str(row["description"]))
        is_nan = value_is_nan(row["description"])

        if description_merged(row) and not is_nan and match:
            reference_no = match[1]
            datetime = match[2]
            description = match[3]

            df.at[index, "reference_no"] = reference_no
            df.at[index, "datetime"] = datetime
            df.at[index, "description"] = description


# %%
split_description(df)
df


# %%
# fix description by merging them and replacing prefix and suffix with NaN
# fix transaction numbers


# %%
# df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %I:%M %p')
# df


# %%
# df.set_index('datetime')


# %%
def fix_description(df):
    for index, row in df.iterrows():
        datetime = row["datetime"]

        try:
            if value_is_nan(datetime):
                prefix = str(df.loc[index]["description"])
                suffix = str(df.loc[index + 2]["description"])
                description = "{} {}".format(prefix, suffix)

                df.at[index + 1, "description"] = description

                df.drop(index=index, inplace=True)
                df.drop(index=index + 2, inplace=True)
        except KeyError:
            pass


#     df.reset_index(inplace=True)
#     df.drop(['index'], axis=1, inplace=True)


# %%
# fix_description(df)
df


# %%
pattern = "to 09954645215"
send_to_mama_filter = df["description"].str.contains(pattern, na=False)
df[send_to_mama_filter]


# %%
credit = df[send_to_mama_filter]["credit"].sum()
credit


# %%
debit = df[send_to_mama_filter]["debit"].sum()
debit


# %%
debit - credit


# %%
xs = df[send_to_mama_filter]["datetime"]
xs


# %%
ys = df[send_to_mama_filter]["debit"]
ys


# %%
plt.plot(xs.apply(str), ys)


# %%
debit_filter = df["debit"] > 0
df[debit_filter]


# %%
plt.plot(df[debit_filter]["datetime"], df[debit_filter]["debit"])


# %%
credit_filter = df["credit"] > 0
df[credit_filter]


# %%
plt.plot(df[credit_filter]["datetime"].apply(str), df[credit_filter]["credit"])


# %%
balance_filter = df["balance"] > 0
df[balance_filter]


# %%
bxs = df[balance_filter]["datetime"].apply(str)
bys = df[balance_filter]["balance"]
plt.plot(bxs, bys)


# %%
mgax = df["datetime"].apply(str)
plt.plot(mgax, df["debit"], mgax, df["credit"], mgax, df["balance"])


# %%
