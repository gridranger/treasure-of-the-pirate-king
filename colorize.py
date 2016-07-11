from PIL.Image import open as pillow_open


def image_tint(src, hex=''):
    if hex == '':
        return pillow_open(src)
    src = pillow_open(src)
    width,height = src.size
    pixel = src.load()
    rgb = (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:], 16))
    for y in range(0, height):
        for x in range(0, width):
            modosito = pixel[x,y][1]/255
            if pixel[x,y][3] > 0:
                pixel[x,y] = (int(rgb[0]*modosito),int(rgb[1]*modosito),int(rgb[2]*modosito),pixel[x,y][3])
    return src
