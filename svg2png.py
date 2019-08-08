from cairosvg.surface import PNGSurface
import os
from PIL import Image
import matplotlib.pyplot as plt
import io
import numpy as np
import glob2
from tqdm import tqdm

def svg2png(in_path, width, height, out_path):
    with open(in_path, 'rb') as svg_file:
        png = PNGSurface.convert(
            bytestring=svg_file.read(),
            width=width,
            height=height
            )
    image = np.array(Image.open(io.BytesIO(png)))[:, :, -1]
    image = Image.fromarray(image)
    w, h = image.size
    ratio = w / float(h)
    new_im = Image.new("L", (64, 64))
    new_size =  (w * 64 // h, 64)
    image = image.resize(new_size, Image.ANTIALIAS)
    new_im.paste(image.convert('L'), ((64-new_size[0])//2, (64-new_size[1])//2))
    plt.imsave(out_path, new_im)


print('globbing paths...')
base_path = '/shared/haofeng/fonts/google-fonts-data'
paths = glob2.glob(os.path.join(base_path, '**/*.svg'))
for filename in tqdm(paths):
    png_dir = os.path.join(*(filename.split('/')[:-2] + ['png']))
    if filename.startswith('/'):
        png_dir = '/' + png_dir
    os.makedirs(png_dir, exist_ok=True)
    png_path = os.path.join(png_dir, filename.split('/')[-1].split('.')[0] + '.png')
    svg2png(filename, 64, 64, png_path)
