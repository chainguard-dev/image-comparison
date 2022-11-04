"""Prepare image CVE data for publishing publicly."""

import logging
import os

import pandas as pd  # pylint: disable=import-error

from filter_data import filter_df

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s",
)

DATA_URL = os.environ.get("DATA_URL")

if __name__ == "__main__":
    logging.info("Starting to read in image cve data")
    df = pd.read_csv(DATA_URL, parse_dates=["time"])
    logging.info("Finished reading in image cve data")

    filtered_df = filter_df(df)

    filtered_df.to_csv("data.csv")
    # pylint: disable=fixme
    # TODO: Commit and push to main
