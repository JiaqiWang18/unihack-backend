from PIL import Image, ImageFilter, ImageOps

import numpy as np
from matplotlib import pyplot as plt

from collections import deque

from cnocr import CnOcr

if __name__ == '__main__':

    # Read image
    filepath = '/Users/jiaqiwang/Downloads/test.jpg'
    im = Image.open(filepath)

    resizeW = 400

    W = im.width
    H = im.height

    im = im.resize((resizeW, int(H / W * resizeW)))
    W = im.width
    H = im.height
    im = im.crop((0, H * 0.08, W, H - H * 0.05))

    im_invert = ImageOps.invert(im)
    new_im = im.convert('L')
    g_im = np.array(new_im)
    res_im = np.array(new_im)

    # print(new_im.getpixel((0,0)))

    W = im.width
    H = im.height

    c_count = []

    percentagelog = []
    for c in range(g_im.shape[1]):
        count = 0
        for r in range(g_im.shape[0]):
            if abs(g_im[r, c] - 237) < 5:
                count += 1
        if count / H > 0.95:
            c_count.append(c)
        percentagelog.append(count / H)

    plt.plot(percentagelog)

    last = 0
    for i in c_count:
        if i > W / 5 and last < W * 4 / 5:
            print(i, last)
            cropright, cropleft = i, last
        last = i

    cropim = im.crop((cropleft, 0, cropright, H))
    c_im = np.array(cropim)
    c_im2 = np.array(cropim)

    CW = cropim.width
    CH = cropim.height


    def is_valid(gridsize, vector, vis):
        max_r, max_c = gridsize
        r, c = vector
        if r < 0 or r >= max_r or c < 0 or c >= max_c:
            return False
        if vector in vis:
            return False
        return True


    def BFS(grid, start):
        directions = (
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)
        )

        vis = []
        q = []
        r, c = start

        min_r, min_c, max_r, max_c = r, c, r, c

        vis.append(start)
        q.append(start)

        while q:
            r, c = current = q.pop(0)
            vis.append(current)
            for d in directions:
                newvec = (r + d[0], c + d[1])
                if is_valid(grid.shape, newvec, vis) and not newvec in q and grid[newvec] == 1:
                    q.append((r + d[0], c + d[1]))
            #         print(r,c)
            if r > max_r: max_r = r
            if c > max_c: max_c = c
            if r < min_r: min_r = r
            if c < min_c: min_c = c

        return min_r, min_c, max_r, max_c


    def fillarr(arr, vec1, vec2):
        r1, c1 = vec1
        r2, c2 = vec2
        for rnum, r in enumerate(arr):
            for cnum, c in enumerate(r):
                if r1 <= rnum <= r2 and c1 <= cnum <= c2:
                    arr[rnum, cnum] = 2


    #                 print(rnum,cnum)

    def fillim(arr, vec1, vec2):
        r1, c1 = vec1
        r2, c2 = vec2
        for rnum, r in enumerate(arr):
            for cnum, c in enumerate(r):
                if r1 <= rnum <= r2 and c1 <= cnum <= c2:
                    arr[rnum, cnum] = np.array([151, 235, 116])


    bitmap = np.zeros((CH, CW))

    for r in range(CH):
        count = 0
        for c in range(CW):
            color = c_im[r, c]
            if np.linalg.norm(color - np.array((151, 235, 116))) < 25:
                c_im2[r, c] = (0, 0, 0)
                bitmap[r, c] = 1

    rnum, cnum = 0, 0
    while rnum < bitmap.shape[0]:
        cnum = 0
        while cnum < bitmap.shape[1]:

            #         if rnum == 700 and cnum==500:print('wtf')
            if bitmap[rnum, cnum] != 0:
                #             print('yo')
                min_r, min_c, max_r, max_c = BFS(bitmap, (rnum, cnum))
                #             print(min_r,min_c,max_r,max_c)
                fillarr(bitmap, (min_r, min_c), (max_r, max_c))
                fillim(c_im, (min_r, min_c), (max_r, max_c))
                rnum = max_r
                cnum = bitmap.shape[1]
            cnum += 1
        rnum += 1
    print(rnum, cnum)

    plt.imshow(bitmap)

    from matplotlib import cm

    Image.fromarray(np.uint8(cm.gist_earth(bitmap) * 255))

    Image.fromarray(c_im)

    ocr = CnOcr(name='def')
    res = ocr.ocr(c_im)
    print("Predicted Chars:")
    for i in res:
        tot = "".join(i)
        print(tot)

    print(res)
