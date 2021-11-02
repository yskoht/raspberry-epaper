import logging

def crop(foreImage, backImage):
    fw, fh = foreImage.size
    bw, bh = backImage.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.info('{:.3f}, {:.3f}'.format(fa, ba))

    # 4:3 ~ 16:9
    if not 1.332 < fa < 1.778:
        return foreImage

    if fa < ba:
        nh = fw / ba
        logging.info('nh: {:.3f}'.format(nh))
        return foreImage.crop((0, (fh - nh) // 2, fw, (fh + nh) // 2))
    else:
        nw = ba * fh
        logging.info('nw: {:.3f}'.format(nw))
        return foreImage.crop(((fw - nw) // 2, 0, (fw + nw) // 2, fh))


def resize(foreImage, backImage):
    fw, fh = foreImage.size
    bw, bh = backImage.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.info('{:.3f}, {:.3f}'.format(fa, ba))

    if fa < ba:
        nw = int(float(bh) / float(fh) * fw)
        return foreImage.resize((nw, bh))
    else:
        nh = int(float(bw) / float(fw) * fh)
        return foreImage.resize((bw, nh))


def fitting(_foreImage, backImage):
    cropped = crop(_foreImage, backImage)
    resized = resize(cropped, backImage)

    w, h = resized.size
    bw, bh = backImage.size

    x = int((bw - w) / 2.0)
    y = int((bh - h) / 2.0)
    backImage.paste(resized, (x, y))

    return backImage