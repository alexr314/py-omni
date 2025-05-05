class OmniFocusError(Exception):
    """Base exception for OmniFocus-related errors."""


class FolderNotFoundError(OmniFocusError):
    """Raised when a specified folder is not found."""


class ProjectNotFoundError(OmniFocusError):
    """Raised when a specified project is not found."""


class TaskNotFoundError(OmniFocusError):
    """Raised when a specified task is not found."""


class AppleScriptExecutionError(OmniFocusError):
    """Raised for general AppleScript execution failures."""
