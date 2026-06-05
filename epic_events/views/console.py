"""Console display helpers."""

from rich.console import Console
from rich.panel import Panel

console = Console()


def print_title(title: str) -> None:
    """Display a title panel."""

    console.print(Panel.fit(title, style="bold cyan"))


def print_success(message: str) -> None:
    """Display a success message."""

    console.print(f"[green]{message}[/green]")


def print_error(message: str) -> None:
    """Display an error message."""

    console.print(f"[red]{message}[/red]")


def print_info(message: str) -> None:
    """Display an info message."""

    console.print(message)
