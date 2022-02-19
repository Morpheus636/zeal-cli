class ZealException(Exception):
    """The base exception for the Zeal CLI project."""

    pass


class DocsetAlreadyInstalledError(ZealException):
    """The docset name passed to docset.install() is already installed."""

    pass


class DocsetNotInstalledError(ZealException):
    """The docset name passed to docset.remove() is not installed, and cannot be removed."""

    pass
