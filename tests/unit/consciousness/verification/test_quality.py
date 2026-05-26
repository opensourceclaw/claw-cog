"""Tests for claw_cog.consciousness.verification.quality."""

import pytest
from claw_cog.consciousness.verification.quality import (
    QualityAssessor,
    QualityResult,
    QualityScore,
)


@pytest.fixture
def qa():
    return QualityAssessor()


class TestQualityAssessor:
    def test_string_output(self, qa):
        result = qa.assess("This is a clear and relevant output.")
        assert result.overall_score in (
            QualityScore.EXCELLENT, QualityScore.GOOD
        )

    def test_empty_string(self, qa):
        result = qa.assess("")
        assert result.overall_score == QualityScore.POOR

    def test_none_output(self, qa):
        result = qa.assess(None)
        assert result.overall_score == QualityScore.POOR

    def test_dict_output(self, qa):
        result = qa.assess({"name": "test", "count": 42})
        # 2-item dict may be FAIR (small collection) based on completeness check
        assert result.overall_score in (
            QualityScore.GOOD, QualityScore.EXCELLENT, QualityScore.FAIR
        )

    def test_list_output(self, qa):
        result = qa.assess(["a", "b", "c"])
        assert result.overall_score in (
            QualityScore.GOOD, QualityScore.EXCELLENT
        )

    def test_completeness_expected_length_met(self, qa):
        result = qa.assess("A" * 100, context={"expected_length": 80})
        assert result.scores["completeness"] == QualityScore.EXCELLENT

    def test_completeness_below_threshold(self, qa):
        result = qa.assess("Hi", context={"expected_length": 100})
        assert result.scores["completeness"] in (
            QualityScore.POOR, QualityScore.FAIR
        )

    def test_clarity_long_output(self, qa):
        result = qa.assess("x" * 2000)
        assert result.scores["clarity"] in (
            QualityScore.FAIR, QualityScore.GOOD
        )

    def test_clarity_structured(self, qa):
        text = "\n".join([f"Line {i}" for i in range(25)])
        result = qa.assess(text)
        assert result.scores["clarity"] in (
            QualityScore.GOOD, QualityScore.EXCELLENT
        )

    def test_safety_password_detected(self, qa):
        result = qa.assess("My password is secret123")
        assert result.scores["safety"] == QualityScore.POOR

    def test_safety_token_detected(self, qa):
        result = qa.assess("Here is the API token: xyz")
        assert result.scores["safety"] in (
            QualityScore.POOR, QualityScore.FAIR
        )

    def test_safety_confidential(self, qa):
        result = qa.assess("This is confidential information")
        assert result.scores["safety"] == QualityScore.FAIR

    def test_safety_clean(self, qa):
        result = qa.assess("The weather is nice today")
        assert result.scores["safety"] == QualityScore.EXCELLENT

    def test_relevance_topic_match(self, qa):
        result = qa.assess("Paris is beautiful", context={"expected_topic": "Paris"})
        assert result.scores["relevance"] == QualityScore.EXCELLENT

    def test_relevance_topic_mismatch(self, qa):
        result = qa.assess("I like dogs", context={"expected_topic": "Paris"})
        assert result.scores["relevance"] == QualityScore.FAIR

    def test_short_output_quality(self, qa):
        result = qa.assess("ab", context={"expected_length": 50})
        assert result.scores["completeness"] in (
            QualityScore.FAIR, QualityScore.POOR
        )
