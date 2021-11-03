from typing import Optional
import typer
from box import Box

import raspberry_epaper.print

def main():
  app = typer.Typer(add_completion=False)


  @app.command()
  def print(
    path: str,
    device: str = typer.Option(
      ...,
      '-d',
      '--device',
      help='waveshare device',
    ),
    qr: Optional[str] = typer.Option(
      None,
      '-q',
      '--qr',
      help='QR code string',
    ),
  ):
    raspberry_epaper.print.process(
      Box(
        path=path,
        device=device,
        qr=qr,
      )
    )

  @app.command()
  def version():
    typer.echo('version')


  app()