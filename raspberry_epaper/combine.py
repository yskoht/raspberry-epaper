import logging


def crop(fore_image, back_image):
    fw, fh = fore_image.size
    bw, bh = back_image.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.debug("Fore image aspect ratio:{:.3f}".format(fa))
    logging.debug("E-paper aspect ratio:{:.3f}".format(ba))

    # 4:3 ~ 16:9
    if not 1.332 < fa < 1.778:
        logging.debug("Fore image was not cropped")
        return fore_image

    if fa < ba:
        nh = fw / ba
        logging.debug("Fore image was cropped {}x{} -> {}x{}".format(fw, fh, fw, nh))
        return fore_image.crop((0, (fh - nh) // 2, fw, (fh + nh) // 2))
    else:
        nw = ba * fh
        logging.debug("Fore image was cropped {}x{} -> {}x{}".format(fw, fh, nw, fh))
        return fore_image.crop(((fw - nw) // 2, 0, (fw + nw) // 2, fh))


def resize(fore_image, back_image):
    fw, fh = fore_image.size
    bw, bh = back_image.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.debug("Fore image aspect ratio:{:.3f}".format(fa))
    logging.debug("E-paper aspect ratio:{:.3f}".format(ba))

    if fa < ba:
        nw = int(float(bh) / float(fh) * fw)
        logging.debug("Fore image was resized {}x{} -> {}x{}".format(fw, fh, nw, bh))
        return fore_image.resize((nw, bh))
    else:
        nh = int(float(bw) / float(fw) * fh)
        logging.debug("Fore image was resized {}x{} -> {}x{}".format(fw, fh, bw, nh))
        return fore_image.resize((bw, nh))


def combine(fore_image, back_image, opt):
    if opt["crop"]:
        logging.debug("Crop")
        pre_processed = crop(fore_image, back_image)
    else:
        logging.debug("No crop")
        pre_processed = fore_image
    resized = resize(pre_processed, back_image)

    w, h = resized.size
    bw, bh = back_image.size

    x = int((bw - w) / 2.0)
    y = int((bh - h) / 2.0)
    logging.debug("Placed ({}, {}), ({}, {})".format(x, y, x + w, y + h))
    back_image.convert('rgb').paste(resized, (x, y))

    return back_image
