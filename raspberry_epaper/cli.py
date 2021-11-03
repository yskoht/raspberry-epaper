import logging
import os
from typing import Optional

import typer
from box import Box

import raspberry_epaper.print

from . import __version__

PKG_DIR = os.path.dirname(__file__)
LOG_FORMAT = "[%(levelname)s](%(filename)s:%(lineno)d:%(funcName)s) %(message)s"


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
            os.path.join(PKG_DIR, "font", "NotoSansJP-Regular.otf"),
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
        if verbose:
            logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT)
        elif silent:
            logging.basicConfig(level=logging.ERROR, format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

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
