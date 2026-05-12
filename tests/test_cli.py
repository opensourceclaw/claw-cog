"""Tests for CLI entry point."""
import pytest
from claw_cog.cli import main


def test_main_output(capsys):
    """Test main() prints usage info."""
    main()
    captured = capsys.readouterr()
    assert "claw-cog" in captured.out
    assert "ConsciousAgent" in captured.out


def test_main_as_script():
    """Test that main can be called without error."""
    assert main() is None
