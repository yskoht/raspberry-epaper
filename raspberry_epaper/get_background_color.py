import logging

TH = 0.2

def key(img, x, y):
    return 'black' if img.getpixel((x, y)) == 0 else 'white'


def get_background_color(image):
    pix = {
        'black': 0,
        'white': 0,
    }

    img = image.convert('1')
    width, height = img.size

    for x in range(0, width):
        pix[key(img, x, 0)] += 1
        pix[key(img, x, height-1)] += 1

    for y in range(0, height):
        pix[key(img, 0, y)] += 1
        pix[key(img, width-1, y)] += 1

    s = width * 2 + height * 2
    b = pix['black']
    w = pix['white']
    r = float(w) / float(s)
    logging.info(
        'width: {}, height: {}, pixel {}, white: {}, black: {}, white rate: {:.3f}'.format(
            width, height, s, w, b, r
        )
    )

    if r < TH:
        return 0
    else:
        return 255