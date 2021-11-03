# Raspberry e-paper utility

A tool to easily use waveshare's e-paper module with Raspberry Pi.

## Install

```sh
pip install raspberry-epaper
```

## Usage

### print

Display the image file.

```sh
# For example, when using 7.5inch e-Paper HAT
$ epaper print --device="epd7in5" picture.png
```

Randomly display the image file in a directory.

```sh
$ epaper print --device="epd7in5" directory
```

Display a text file.

```sh
$ epaper print --device="epd7in5" sentence.txt
```

Overlay the QR code on the image.

```sh
$ epaper print --device="epd7in5" --qr="information about the picture" picture.png
```

### version

Show version.

```sh
$ epaper version
0.1.0
```

## License

This software is released under the MIT License, see LICENSE.
Fonts are licensed under the SIL Open Font License, Version 1.1.
