"""Unit testing

Usage:

python test.py
"""

import os
import unittest

import pandas as pd  # pylint: disable=import-error

from filter_data import filter_df

DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class TestFilterDataFunctions(unittest.TestCase):
    # T
    """Test trivy-related functions."""

    def test_filter_df(self):
        """Test filter_df()."""
        # pylint: disable=invalid-name
        TEST_INPUT_DATA = os.path.join(DIR_PATH, "test_data", "test_input_data.csv")
        TEST_EXPECTED_DATA = os.path.join(
            DIR_PATH, "test_data", "test_expected_data.csv"
        )
        input_df = pd.read_csv(TEST_INPUT_DATA, parse_dates=["time"])
        df_got = filter_df(input_df, starting_day="2022-11-01", ending_day="2022-11-03")
        df_expected = pd.read_csv(TEST_EXPECTED_DATA, parse_dates=["time"])
        df_expected_filtered = filter_df(
            df_expected, starting_day="2022-11-01", ending_day="2022-11-03"
        )
        pd.testing.assert_frame_equal(df_got, df_expected_filtered)


if __name__ == "__main__":
    unittest.main()
