import numpy as np
import pandas as pd
import pytest

import seismometer.data.performance as undertest

ALL_STATS = [undertest.THRESHOLD] + undertest.STATNAMES + ["NNT@0.333"]

TEST_KEY_ORDER = [
    "Threshold",
    "TP",
    "FP",
    "TN",
    "FN",
    "Accuracy",
    "Sensitivity",
    "Specificity",
    "PPV",
    "NPV",
    "Flag Rate",
    "LR+",
    "NNE",
    "NetBenefitScore",
    "NNT@0.333",
]


def stats_case_base():
    y_true = np.array([1, 1, 0])
    y_prob = np.array([0.1, 0.5, 0.1])

    expected = []
    # Threshold, TP, FP, TN, FN, Acc, Sens, Spec, PPV, NPV, Flag Rate, LR+, NNE, NBS, NNT1/3 |  Threshold
    expected.append([100, 0, 0, 1, 2, 1 / 3, 0, 1, 1, 1 / 3, 0, np.nan, 1, np.nan, 3])  # 1
    expected.append([50, 1, 0, 1, 1, 2 / 3, 0.5, 1, 1, 0.5, 1 / 3, np.inf, 1, 1 / 3, 3])  # .5
    expected.append([10, 2, 1, 0, 0, 2 / 3, 1, 0, 2 / 3, 1, 1, 1, 1.5, 17 / 27, 4.5])  # .1
    expected.append([0, 2, 1, 0, 0, 2 / 3, 1, 0, 2 / 3, 1, 1, 1, 1.5, 2 / 3, 4.5])  # 0

    return y_true, y_prob, pd.DataFrame(expected, columns=TEST_KEY_ORDER)


def stats_case_0():
    "include prediction of exactly 0"
    y_true = np.array([0, 1, 1, 0])
    y_prob = np.array([0, 0.1, 0.5, 0.1])

    expected = []
    # Threshold, TP, FP, TN, FN, Acc, Sens, Spec, PPV, NPV, Flag Rate, LR+, NNE, NBS, NNT1/3 |  Threshold
    expected.append([100, 0, 0, 2, 2, 0.5, 0, 1, 1, 0.5, 0, np.nan, 1, np.nan, 3])  # 1
    expected.append([50, 1, 0, 2, 1, 0.75, 0.5, 1, 1, 2 / 3, 0.25, np.inf, 1, 1 / 4, 3])  # .5
    expected.append([10, 2, 1, 1, 0, 0.75, 1, 0.5, 2 / 3, 1, 0.75, 2, 1.5, 17 / 36, 4.5])  # .1
    expected.append([0, 2, 2, 0, 0, 0.5, 1, 0, 0.5, 1, 1, 1, 2, 1 / 2, 6])  # 0

    return y_true, y_prob, pd.DataFrame(expected, columns=TEST_KEY_ORDER)


def stats_case_1():
    "include prediction of exactly 1"
    y_true = np.array([1, 1, 0, 1])
    y_prob = np.array([0.1, 0.5, 0.1, 1])

    expected = []
    # Threshold, TP, FP, TN, FN, Acc, Sens, Spec, PPV, NPV, Flag Rate, LR+, NNE, NBS, NNT1/3 |  Threshold
    expected.append([100, 1, 0, 1, 2, 0.5, 1 / 3, 1, 1, 1 / 3, 0.25, np.inf, 1, np.nan, 3])  # 1
    expected.append([50, 2, 0, 1, 1, 0.75, 2 / 3, 1, 1, 0.5, 0.5, np.inf, 1, 1 / 2, 3])  # .5
    expected.append([10, 3, 1, 0, 0, 0.75, 1, 0, 0.75, 1, 1, 1, 4 / 3, 13 / 18, 4])  # .1
    expected.append([0, 3, 1, 0, 0, 0.75, 1, 0, 0.75, 1, 1, 1, 4 / 3, 3 / 4, 4])  # 0

    return y_true, y_prob, pd.DataFrame(expected, columns=TEST_KEY_ORDER)


def stats_case_01():
    "include predictions of exactly 0 and 1"
    y_true = np.array([0, 1, 1, 0, 1])
    y_prob = np.array([0, 0.1, 0.5, 0.1, 1])

    expected = []
    # Threshold, TP, FP, TN, FN, Acc, Sens, Spec, PPV, NPV, Flag Rate, LR+, NNE, NBS, NNT1/3 |  Threshold
    expected.append([100, 1, 0, 2, 2, 0.6, 1 / 3, 1, 1, 0.5, 0.2, np.inf, 1, np.nan, 3])  # 1
    expected.append([50, 2, 0, 2, 1, 0.8, 2 / 3, 1, 1, 2 / 3, 0.4, np.inf, 1, 2 / 5, 3])  # .5
    expected.append([10, 3, 1, 1, 0, 0.8, 1, 0.5, 0.75, 1, 0.8, 2, 4 / 3, 26 / 45, 4])  # .1
    expected.append([0, 3, 2, 0, 0, 0.6, 1, 0, 0.6, 1, 1, 1, 5 / 3, 3 / 5, 5])  # 0

    return y_true, y_prob, pd.DataFrame(expected, columns=TEST_KEY_ORDER)


def stats_case_0_4():
    y_true = np.array([1, 1, 0, 0])
    y_prob = np.array([0.75, 0.5, 0.25, 0])

    expected = []
    # Threshold, TP, FP, TN, FN, Acc, Sens, Spec, PPV, NPV, Flag Rate, LR+, NNE, NBS, NNT1/3 |  Threshold
    expected.append([100, 0, 0, 2, 2, 0.5, 0, 1, 1, 0.5, 0, np.nan, 1, np.nan, 3])  # 1
    expected.append([75, 1, 0, 2, 1, 0.75, 0.5, 1, 1, 2 / 3, 0.25, np.inf, 1, 1 / 4, 3])  # .75
    expected.append([50, 2, 0, 2, 0, 1, 1, 1, 1, 1, 0.5, np.inf, 1, 1 / 2, 3])  # .5
    expected.append([25, 2, 1, 1, 0, 0.75, 1, 0.5, 2 / 3, 1, 0.75, 2, 1.5, 5 / 12, 4.5])  # .25
    expected.append([0, 2, 2, 0, 0, 0.5, 1, 0, 0.5, 1, 1, 1, 2, 1 / 2, 6])  # 0

    return (y_true, y_prob, pd.DataFrame(expected, columns=TEST_KEY_ORDER))


@pytest.mark.parametrize(
    "y_true,y_prob,expected",
    [stats_case_base(), stats_case_0(), stats_case_1(), stats_case_01(), stats_case_0_4()],
    ids=["base", "0-pred", "1-pred", "1 and 0 preds", "0 preds"],
)
class Test_Stats:
    def test_stat_keys(self, y_true, y_prob, expected):
        """Ensure stat manipulations are intentional"""
        expected_keys = {
            "Flag Rate",
            "Accuracy",
            "Sensitivity",
            "Specificity",
            "PPV",
            "NPV",
            "LR+",
            "NNE",
            "NetBenefitScore",
            "TP",
            "FP",
            "TN",
            "FN",
        }
        assert set(undertest.STATNAMES) == expected_keys

    def test_score_arr(self, y_true, y_prob, expected):
        actual = undertest.calculate_bin_stats(y_true, y_prob, not_point_thresholds=True)
        assert ALL_STATS == list(actual)
        pd.testing.assert_frame_equal(actual, expected, check_column_type=False, check_like=True, check_dtype=False)

    def test_score_arr_percentile(self, y_true, y_prob, expected):
        y_prob = y_prob * 100
        actual = undertest.calculate_bin_stats(y_true, y_prob, not_point_thresholds=True)
        assert ALL_STATS == list(actual)
        pd.testing.assert_frame_equal(actual, expected, check_column_type=False, check_like=True, check_dtype=False)

    def test_score_with_y_proba_nulls(self, y_true, y_prob, expected):
        y_prob = np.hstack((y_prob, [np.nan, np.nan]))
        y_true = np.hstack((y_true, [0, 1]))
        actual = undertest.calculate_bin_stats(y_true, y_prob, not_point_thresholds=True)
        assert ALL_STATS == list(actual)
        pd.testing.assert_frame_equal(actual, expected, check_column_type=False, check_like=True, check_dtype=False)

    def test_score_with_y_true_nulls(self, y_true, y_prob, expected):
        y_prob = np.hstack((y_prob, [0.1, 0.9]))
        y_true = np.hstack((y_true, [np.nan, np.nan]))
        actual = undertest.calculate_bin_stats(y_true, y_prob, not_point_thresholds=True)
        assert ALL_STATS == list(actual)
        pd.testing.assert_frame_equal(actual, expected, check_column_type=False, check_like=True, check_dtype=False)


def test_bin_stats_point_thresholds():
    y_true, y_prob, base_expected = stats_case_base()
    actual = undertest.calculate_bin_stats(y_true, np.array(y_prob))

    expected = []
    for dup, row in zip([50, 40, 11], base_expected.iterrows()):
        expected.extend([row[1]] * dup)
    expected = pd.DataFrame(expected)
    expected.Threshold = np.arange(100, -1, -1)
    expected = expected.reset_index(drop=True)

    # Verify accuracy of threshold point-wise in above cases,
    # duplication doesn't apply
    threshold_dependent_columns = ["NetBenefitScore"]
    expected = expected.drop(columns=threshold_dependent_columns)
    actual = actual.drop(columns=threshold_dependent_columns)

    pd.testing.assert_frame_equal(actual, expected[actual.columns], check_dtype=False)


def test_threshold_precision_increases_rows():
    y_true = np.array([1, 0])
    y_prob = np.array([0.5, 0.3])

    # Use default threshold precision (0): 101 rows (0–100)
    default_stats = undertest.calculate_bin_stats(y_true, y_prob)
    assert len(default_stats) == 101

    # Now try precision=2 → 10,001 thresholds
    high_precision_stats = undertest.calculate_bin_stats(y_true, y_prob, threshold_precision=2)
    assert len(high_precision_stats) == 100 * 10**2 + 1


def test_thresholds_are_rounded_correctly():
    y_true = np.array([1, 0])
    y_prob = np.array([0.6, 0.3])
    threshold_precision = 2

    stats = undertest.calculate_bin_stats(y_true, y_prob, threshold_precision=threshold_precision)
    thresholds = stats["Threshold"].to_numpy()

    step = 1 / 10**threshold_precision
    assert np.allclose(np.diff(thresholds[::-1]), step, atol=1e-6)


def test_all_metrics_valid_with_high_threshold_precision():
    y_true = np.array([1, 1, 0, 0])
    y_prob = np.array([0.9, 0.7, 0.4, 0.2])

    stats = undertest.calculate_bin_stats(y_true, y_prob, threshold_precision=2)

    all_metrics = undertest.STATNAMES + [f"NNT@{undertest.DEFAULT_RHO:0.3n}"]

    for metric in all_metrics:
        assert metric in stats.columns
        values = stats[metric].dropna()

        if metric in {"Accuracy", "Sensitivity", "Specificity", "PPV", "NPV", "Flag Rate"}:
            assert (0.0 <= values).all() and (values <= 1.0).all()

        elif metric in {"TP", "FP", "TN", "FN"}:
            assert (values >= 0).all()
            assert pd.api.types.is_integer_dtype(values)

        elif metric in {"LR+", "NetBenefitScore", "NNE", f"NNT@{undertest.DEFAULT_RHO:0.3n}"}:
            finite_values = values[np.isfinite(values)]
            assert (finite_values >= 0).all()

        else:
            assert pd.api.types.is_numeric_dtype(values)


def sumall(a, b):
    return a.sum() + b.sum()


def sumdiff(a, b):
    return (a - b).sum()


class Test_AsProbabilities:
    def test_convert(self):
        percentages = np.random.uniform(low=0, high=100, size=100)
        expected = percentages / 100
        assert np.array_equal(undertest.as_probabilities(percentages), expected)

    def test_already_in_range(self):
        percentages = np.random.uniform(low=0, high=1, size=100)
        assert np.array_equal(undertest.as_probabilities(percentages), percentages)


class Test_AsPercentages:
    def test_convert(self):
        percentages = np.random.uniform(low=0, high=1, size=100)
        expected = percentages * 100
        assert np.array_equal(undertest.as_percentages(percentages), expected)

    def test_already_in_range(self):
        percentages = np.random.uniform(low=0, high=100, size=100)
        assert np.array_equal(undertest.as_percentages(percentages), percentages)
