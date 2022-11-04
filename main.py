"""Prepare image CVE data for publishing publicly."""

import os

import pandas as pd  # pylint: disable=import-error

from filter_data import filter_df

DATA_URL = os.environ.get("DATA_URL")

if __name__ == "__main__":
    df = pd.read_csv(DATA_URL, parse_dates=["time"])
    filtered_df = filter_df(df)
    filtered_df.to_csv("data.csv")
    # pylint: disable=fixme
    # TODO: Commit and push to main
