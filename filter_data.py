"""Filter base image CVE data before publication."""

import logging

from datetime import datetime, timedelta


def filter_df(dataframe, starting_day=None, ending_day=None):
    """Filter pandas dataframe before publication.

    Filters include:
      -trivy results only
      -32 days to 2 days ago (to allow time for debugging if issues arises)
      -nginx, php, and go images (cgr.dev and Docker Hub equivalents)

    Args:
        dataframe (pandas dataframe)
        starting_day (time) - day on which to begin filtering data
        ending_day (time) - day on which to stop filtering data

    Returns:
        filtered_df (pandas dataframe)
    """
    logging.info("Starting filtering operation")

    today = datetime.today()
    logging.info("today: %s", today)
    if starting_day is None:
        # set to 32 days ago
        starting_day = today - timedelta(days=32)
    if ending_day is None:
        # set to 2 days ago
        ending_day = today - timedelta(days=2)
    logging.info("starting_day: %s", starting_day)
    logging.info("ending_day: %s", ending_day)

    # Filter in only trivy scan results
    filtered_df = dataframe[dataframe["scanner"] == "trivy"]

    # Filter in observations between certain dates
    filtered_df = filtered_df[
        (filtered_df["time"] >= starting_day) & (filtered_df["time"] <= ending_day)
    ]

    # filter in only nginx, php, and go images
    # (both chainguard images version and Dockerhub equivalent)
    # pylint: disable=invalid-name
    IMAGE_LIST = [
        "cgr.dev/chainguard/php:latest",
        "cgr.dev/chainguard/go:latest",
        "cgr.dev/chainguard/nginx:latest",
        "php:latest",
        "nginx:latest",
        "golang:latest",
    ]
    filtered_df = filtered_df[filtered_df["image"].isin(IMAGE_LIST)]

    # drop "success" column since that is only interesting for
    # internal chainguard quality control purposes
    # drop negligible_cve_cnt since that is a grype-related column and
    # doesn't apply to trivy scans
    filtered_df = filtered_df.drop(columns=["success", "negligible_cve_cnt"])

    # reset index (done to enable reproducibility during testing)
    filtered_df = filtered_df.reset_index(drop=True)

    logging.info("Finished filtering operation")
    return filtered_df
