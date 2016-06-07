import PIL
from PIL.Image import open

def image_tint(src, hex=''):
    if hex == '':
        return open(src)
    src = open(src)
    width,height = src.size
    pixel = src.load()
    rgb = (int(hex[1:3], 16), int(hex[3:5], 16), int(hex[5:], 16))
    for y in range(0, height):
        for x in range(0, width):
            modosito = pixel[x,y][1]/255
            if pixel[x,y][3] > 0:
                pixel[x,y] = (int(rgb[0]*modosito),int(rgb[1]*modosito),int(rgb[2]*modosito),pixel[x,y][3])
    return src
    
if __name__ == '__main__':
    import os

    input_image_path = 'piszkozatok/schooner-z.png'
    print('tinting "{}"'.format(input_image_path))

    root, ext = os.path.splitext(input_image_path)
    result_image_path = root+'_result'+ext

    print('creating "{}"'.format(result_image_path))
    result = image_tint(input_image_path, '#aaffaa')
    if os.path.exists(result_image_path):  # delete any previous result file
        os.remove(result_image_path)
    result.save(result_image_path)  # file name's extension determines format

    print('done')