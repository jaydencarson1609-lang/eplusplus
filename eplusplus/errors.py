class EppError(Exception):
    """Base error for E++."""

    def __init__(self, message: str, line: int | None = None):
        self.line = line
        if line is not None:
            super().__init__(f"Line {line}: {message}")
        else:
            super().__init__(message)


class EppSyntaxError(EppError):
    pass


class EppRuntimeError(EppError):
    pass
