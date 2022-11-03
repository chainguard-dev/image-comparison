"""Filter base image CVE data before publication."""

import os

import pandas as pd

def filter_df(df, starting_day=None, ending_day=None):
    """Filter pandas dataframe before publication.

    Filters include:
      -trivy results only
      -32 days to 2 days ago (to allow time for debugging if issues arises)
      -nginx, php, and go images (cgr.dev and Docker Hub equivalents)

    Args:
        df (pandas dataframe)
        starting_day (time)
        ending_day (time)

    Returns:
        filtered_df (pandas dataframe)
    """

    if starting_day is not None:
        # set to 32 days ago
        pass
    if ending_day is not None:
        # set to 2 days ago
        pass

    # Filter in only trivy scan results
    filtered_df = df[df["scanner"] == "trivy"]

    # Filter in observations between certain dates
    # TODO: use starting_day and ending_day
    filtered_df = filtered_df[(filtered_df["time"] >= "2022-08-16") & (filtered_df["time"] <= "2022-09-15")]

    # filter in only nginx, php, and go images
    # (both chainguard images version and Dockerhub equivalent)
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

    return filtered_df
