import logging

def fitting(foreImage, backImage):
    fw, fh = foreImage.size
    bw, bh = backImage.size

    fa = float(fw) / float(fh)
    ba = float(bw) / float(bh)

    logging.info('{:.3f}, {:.3f}'.format(fa, ba))

    if fa < ba:
        nw = int(float(bh) / float(fh) * fw)
        img = foreImage.resize((nw, bh))
    else:
        nh = int(float(bw) / float(fw) * fh)
        img = foreImage.resize((bw, nh))

    w, h = img.size
    x = int((bw - w) / 2.0)
    y = int((bh - h) / 2.0)
    backImage.paste(img, (x, y))
    return backImage