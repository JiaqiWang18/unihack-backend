#!/usr/bin/env python
# coding: utf-8

from PIL import Image

import numpy as np
from matplotlib import pyplot as plt

from cnocr import CnOcr

def ImageToText:
    # Read image
    filepath = "../Capture.JPG"
    im = Image.open(filepath)

    im = im.convert("RGB")

    resizeW = 400

    W = im.width
    H = im.height

    im = im.resize((resizeW, int(H / W * resizeW)))
    W = im.width
    H = im.height
    im = im.crop((0, H * 0.08, W, H - H * 0.05))


    new_im = im.convert('L')
    g_im = np.array(new_im)
    res_im = np.array(new_im)


    W = im.width
    H = im.height

    c_count = []

    percentagelog = []
    for c in range(g_im.shape[1]):
        count = 0
        for r in range(g_im.shape[0]):
            if abs(g_im[r, c] - 243) < 5:  # 43
                count += 1
        if count / H > 0.95:
            c_count.append(c)
        percentagelog.append(count / H)

    pcl = percentagelog

    cropleft = 0
    for i in range(3, int(len(pcl) / 5)):
        if (pcl[i - 1] + pcl[i - 2]) / 2 - (pcl[i] + pcl[i + 1]) / 2 > 0.05:
            cropleft = i
    cropright = W
    for i in range(len(pcl) - 3, int(len(pcl) * 4 / 5), -1):
        if (pcl[i] + pcl[i + 1]) / 2 - (pcl[i - 1] + pcl[i - 2]) / 2 > 0.05:
            cropright = i


    plt.plot(percentagelog)



    cropim = im.crop((cropleft, 0, cropright, H))
    c_im = np.array(cropim)
    c_im2 = np.array(cropim)

    CW = cropim.width
    CH = cropim.height


    bitmap = np.zeros((CH, CW))

    for r in range(CH):
        count = 0
        for c in range(CW):
            color = c_im[r, c]
            if np.linalg.norm(color - np.array((151, 235, 116))) < 25:
                c_im2[r, c] = (0, 0, 0)
                bitmap[r, c] = 1


    percentcounter = [0, 0]
    diffcounter = []
    sep = []

    for r in range(CH):
        count = 0
        for c in range(CW):
            color = c_im[r, c]
            if np.linalg.norm(color - np.array((255, 255, 255))) < 10:
                c_im2[r, c] = (0, 255, 0)
                count += 1
        percentcounter.append(count / CW)

        diffcounter.append(abs(percentcounter[-1] - percentcounter[-2]))

        if len(percentcounter) > 4 and percentcounter[-1] - (
                percentcounter[-2] + percentcounter[-3] + percentcounter[-4]) / 3 > 0.1 and min(percentcounter[-1],
                                                                                                percentcounter[-2],
                                                                                                percentcounter[-3],
                                                                                                percentcounter[-4]) < 0.05:
            sep.append([r, 0])
        if len(percentcounter) > 4 and (percentcounter[-2] + percentcounter[-3] + percentcounter[-4]) / 3 - percentcounter[
            -1] > 0.1 and min(percentcounter[-1], percentcounter[-2], percentcounter[-3], percentcounter[-4]) < 0.05:
            sep.append([r, 1])

    # In[23]:


    sep2 = []
    index = 0
    while index < len(sep) - 1:
        if sep[index + 1][1] == sep[index][1]:
            sep.pop(index + 1)
        else:
            index += 1
    if sep[-1][1] == 0:
        sep = sep[:-1]
    error = False
    for i in range(len(sep) - 1):
        if sep[i] == sep[i + 1]:
            error = True
    assert not error
    pairs = []
    for i in range(0, len(sep) - 1, 2):
        pairs.append((sep[i][0], sep[i + 1][0]))

    lines = []
    ocr = CnOcr(name='def')
    for pair in pairs:
        text = ocr.ocr(c_im[pair[0]:pair[1], ])
        line = []
        for i in text:
            line.append("".join(i).strip())
        total = "".join(line).strip()
        lines.append(total)
        print(total)

    Image.fromarray(c_im[pairs[0][0]:pairs[0][1], ])
