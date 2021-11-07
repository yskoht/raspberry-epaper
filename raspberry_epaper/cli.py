import logging
import os
from typing import Optional

import typer
from box import Box

import raspberry_epaper.print
from raspberry_epaper.epd import EPD
from raspberry_epaper.type import Device, Order

from . import __version__

PKG_DIR = os.path.dirname(__file__)
LOG_FORMAT = (
    "%(asctime)s [%(levelname)s](%(filename)s:%(lineno)d:%(funcName)s) %(message)s"
)


def main():
    app = typer.Typer(add_completion=False)

    @app.command()
    def print(
        path: str,
        crop: bool = typer.Option(
            True,
            "--crop/--no-crop",
            help="Crop image",
        ),
        device: Device = typer.Option(
            ...,
            "-d",
            "--device",
            help="Waveshare device",
        ),
        font: str = typer.Option(
            os.path.join(PKG_DIR, "font", "NotoSansJP-Regular.otf"),
            "--font",
            help="Font file",
        ),
        font_size: int = typer.Option(
            12,
            "--font-size",
            help="Font size",
        ),
        order: Order = typer.Option(
            Order.random,
            "--order",
            help="Order of files",
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
                crop=crop,
                device=device,
                font=font,
                font_size=font_size,
                order=order,
                qr=qr,
            )
        )

    @app.command()
    def version():
        typer.echo(__version__)

    @app.command()
    def modules():
        for module in EPD.modules():
            typer.echo(module)

    app()
