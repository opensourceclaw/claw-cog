"""Custom exceptions for claw-cog."""


class ClawCogError(Exception):
    """Base exception for all claw-cog errors."""


class ConfigurationError(ClawCogError):
    """Configuration validation error."""


class LayerError(ClawCogError):
    """Layer processing error."""


class WorkspaceError(ClawCogError):
    """Global workspace error."""


class AssessmentError(ClawCogError):
    """Assessment error."""
