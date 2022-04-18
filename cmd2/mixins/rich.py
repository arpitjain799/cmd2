import sys
from typing import (
    Any,
)

from rich import Console

try:
    from typing import (
        Protocol,
        runtime_checkable,
)
except ImportError:
    from typing_extensions import (  # type: ignore[misc]
        Protocol,
        runtime_checkable,
    )


class Cmd2PrintProtocol(Protocol):
    debug: bool

    def poutput(self, msg: Any = '', *, end: str = '\n') -> None:
        """Print message to self.stdout and appends a newline by default

        Also handles BrokenPipeError exceptions for when a command's output has
        been piped to another process and that process terminates before the
        cmd2 command is finished executing.

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        """

    # noinspection PyMethodMayBeStatic
    def perror(self, msg: Any = '', *, end: str = '\n', apply_style: bool = True) -> None:
        """Print message to sys.stderr

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """

    def pwarning(self, msg: Any = '', *, end: str = '\n', apply_style: bool = True) -> None:
        """Wraps perror, but applies ansi.style_warning by default

        :param msg: object to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_warning will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """

    def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
        """Print Exception message to sys.stderr. If debug is true, print exception traceback if one exists.

        :param msg: message or Exception to print
        :param end: string appended after the end of the message, default a newline
        :param apply_style: If True, then ansi.style_error will be applied to the message text. Set to False in cases
                            where the message text already has the desired style. Defaults to True.
        """


class RichCmd(Cmd2PrintProtocol):
    """
    Mixin class that swaps out the cmd2.Cmd output calls to use the ``rich`` library.

    NOTE: Mixin classes should be placed to the left of the base Cmd class in the inheritance declaration.
    """
    def __init__(self, *args, **kwargs) -> None:
        super(RichCmd, self).__init__(*args, **kwargs)
        self.rich_out = Console(file=self.stdout)
        self.rich_err = Console(stderr=True)

    def pexcept(self, msg: Any, *, end: str = '\n', apply_style: bool = True) -> None:
        if self.debug and sys.exc_info() != (None, None, None):
            self.rich_err.print_exception(show_locals=True)
        else:
            super().pexcept(msg, end=end, apply_style=apply_style)




