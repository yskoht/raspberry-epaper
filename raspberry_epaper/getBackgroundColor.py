import logging

def getBackgroundColor(image):
    w = 0
    b = 0
    s = 0

    img = image.convert('1')
    width, height = img.size
    for x in range(0, width):
        p = img.getpixel((x, 0))
        s += 1
        if p == 0:
            b += 1
        else:
            w += 1
    for x in range(0, width):
        p = img.getpixel((x, height-1))
        s += 1
        if p == 0:
            b += 1
        else:
            w += 1
    for y in range(0, height):
        p = img.getpixel((0, y))
        s += 1
        if p == 0:
            b += 1
        else:
            w += 1
    for y in range(0, height):
        p = img.getpixel((width-1, y))
        s += 1
        if p == 0:
            b += 1
        else:
            w += 1

    r = float(w) / float(s)
    logging.info(
        'width: {}, height: {}, pixel {}({}), white: {}, black: {}, white rate: {:.3f}'.format(
            width, height, width * 2 + height * 2, s, w, b, r
        )
    )

    if r < 0.2:
        return 0
    else:
        return 255