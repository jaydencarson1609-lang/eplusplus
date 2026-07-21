"""E++ (English++) — write code in plain English."""

from .interpreter import Interpreter
from .errors import EppError, EppRuntimeError, EppSyntaxError

__all__ = ["Interpreter", "EppError", "EppRuntimeError", "EppSyntaxError"]
__version__ = "0.5.0"
