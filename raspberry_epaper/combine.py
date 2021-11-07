import logging


def crop(foreImage, backImage):
    fw, fh = foreImage.size
    bw, bh = backImage.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.debug("Foreimage aspect ratio:{:.3f}".format(fa))
    logging.debug("E-paper aspect ratio:{:.3f}".format(ba))

    # 4:3 ~ 16:9
    if not 1.332 < fa < 1.778:
        logging.debug("Foreimage was not cropped")
        return foreImage

    if fa < ba:
        nh = fw / ba
        logging.debug("Foreimage was cropped {}x{} -> {}x{}".format(fw, fh, fw, nh))
        return foreImage.crop((0, (fh - nh) // 2, fw, (fh + nh) // 2))
    else:
        nw = ba * fh
        logging.debug("Foreimage was cropped {}x{} -> {}x{}".format(fw, fh, nw, fh))
        return foreImage.crop(((fw - nw) // 2, 0, (fw + nw) // 2, fh))


def resize(foreImage, backImage):
    fw, fh = foreImage.size
    bw, bh = backImage.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.debug("Foreimage aspect ratio:{:.3f}".format(fa))
    logging.debug("E-paper aspect ratio:{:.3f}".format(ba))

    if fa < ba:
        nw = int(float(bh) / float(fh) * fw)
        logging.debug("Foreimage was resized {}x{} -> {}x{}".format(fw, fh, nw, bh))
        return foreImage.resize((nw, bh))
    else:
        nh = int(float(bw) / float(fw) * fh)
        logging.debug("Foreimage was resized {}x{} -> {}x{}".format(fw, fh, bw, nh))
        return foreImage.resize((bw, nh))


def combine(foreImage, backImage, opt):
    if opt["crop"]:
        logging.debug("Crop")
        pre_processed = crop(foreImage, backImage)
    else:
        logging.debug("No crop")
        pre_processed = foreImage
    resized = resize(pre_processed, backImage)

    w, h = resized.size
    bw, bh = backImage.size

    x = int((bw - w) / 2.0)
    y = int((bh - h) / 2.0)
    logging.debug("Placed ({}, {}), ({}, {})".format(x, y, x + w, y + h))
    backImage.paste(resized, (x, y))

    return backImage
