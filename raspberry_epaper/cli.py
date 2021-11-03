import logging
import os
from typing import Optional

import typer
from box import Box

import raspberry_epaper.print

from . import __version__, pkg_dir


def main():
    app = typer.Typer(add_completion=False)

    @app.command()
    def print(
        path: str,
        device: str = typer.Option(
            ...,
            "-d",
            "--device",
            help="waveshare device",
        ),
        font: str = typer.Option(
            os.path.join(pkg_dir, "font", "NotoSansJP-Regular.otf"),
            "--font",
            help="font file",
        ),
        font_size: int = typer.Option(
            12,
            "--font-size",
            help="font size",
        ),
        qr: Optional[str] = typer.Option(
            None,
            "--qr",
            help="QR code string",
        ),
        silent: bool = typer.Option(
            False,
            "--silent",
            help="Hide log",
        ),
        verbose: bool = typer.Option(
            False,
            "--verbose",
            help="Show debug log",
        ),
    ):
        logging.basicConfig(level=logging.INFO)
        if silent:
            logging.basicConfig(level=logging.ERROR)
        if verbose:
            logging.basicConfig(leven=logging.DEBUG)

        raspberry_epaper.print.process(
            Box(
                path=path,
                device=device,
                font=font,
                font_size=font_size,
                qr=qr,
            )
        )

    @app.command()
    def version():
        typer.echo(__version__)

    app()
