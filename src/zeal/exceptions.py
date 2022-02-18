class ZealException(Exception):
    """The base exception for the Zeal CLI project."""

    pass


class DocsetAlreadyInstalledError(ZealException):
    """The docset name passed to docset.install() is already installed."""

    pass
