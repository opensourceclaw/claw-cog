"""Tests for claw_cog.consciousness.verification.consistency."""

import pytest
from dataclasses import dataclass
from claw_cog.consciousness.verification.consistency import (
    ConsistencyChecker,
    ConsistencyResult,
)


@pytest.fixture
def checker():
    return ConsistencyChecker(deviation_threshold=0.3)


@dataclass
class FakeResult:
    output: str


class TestConsistencyChecker:
    def test_empty_history(self, checker):
        result = checker.check("hello", [])
        assert result.is_consistent
        assert result.contradictions == []
        assert result.deviation_score == 0.0

    def test_consistent_output(self, checker):
        history = [
            FakeResult(output="Paris is the capital of France"),
            FakeResult(output="The Eiffel Tower is in Paris"),
        ]
        result = checker.check("Paris is a beautiful city", history)
        assert result.is_consistent

    def test_contradiction_detected(self, checker):
        history = [
            FakeResult(output="The answer is Paris"),
        ]
        result = checker.check("The answer is not Paris", history)
        assert not result.is_consistent or len(result.contradictions) > 0

    def test_deviation_score(self, checker):
        history = [
            FakeResult(output="The answer is Paris"),
            FakeResult(output="The answer is London"),
        ]
        result = checker.check("The answer is not Paris", history)
        assert 0.0 <= result.deviation_score <= 1.0

    def test_history_deviation(self, checker):
        history = [
            FakeResult(output="Topic A: cats are great"),
            FakeResult(output="Topic A: cats are lovely"),
        ]
        result = checker.check("Topic A: cats are not great", history)
        assert result.deviation_score >= 0.0

    def test_dict_result(self, checker):
        history = [
            FakeResult(output="Cats are great"),
        ]
        result = checker.check({"output": "Cats are not great"}, history)
        assert result.deviation_score >= 0.0

    def test_none_result(self, checker):
        result = checker.check(None, [FakeResult(output="something")])
        assert result.is_consistent

    def test_no_contradiction_similar(self, checker):
        history = [
            FakeResult(output="Cats are great"),
        ]
        result = checker.check("Cats are great", history)
        assert result.contradictions == []

    def test_multiple_history_contradictions(self, checker):
        history = [
            FakeResult(output="Apples are red"),
            FakeResult(output="The sky is blue"),
            FakeResult(output="Water is wet"),
        ]
        result = checker.check("Apples are not red", history)
        assert len(result.contradictions) > 0
