"""Prepare image CVE data for publishing publicly."""

import os

import pandas as pd

from filter_data import filter_df

# Details about bucket from which to download images CVE data
BUCKET = os.environ.get("BUCKET")

if __name__ == "__main__":
    df = pd.read_csv(f"gs://{BUCKET}/latest.csv")
    filtered_df = filter_df(df)
    filtered_df.to_csv("data.csv", parse_dates=["time"])
    # TODO: Commit and push to main
