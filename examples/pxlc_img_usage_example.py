
import os
import sys

PXLC_TD_ROOT = '/'.join(os.path.abspath(__file__).replace('\\','/').split('/')[:-2])

sys.path.append(PXLC_TD_ROOT)
import pxlc.img

from PIL import Image


if __name__ == '__main__':

    in_img = Image.open('%s/examples/data/rendered_frame.png' % PXLC_TD_ROOT)
    w_bkg_img = pxlc.img.add_color_bkg_to_image( in_img, (127, 127, 127, 255) )

    tovr = pxlc.img.TextOverlay('rgba(255, 255, 255, 255)', 'rgba(0, 0, 0, 255)', 1)

    tovr.add_text_item('Hello World!', 20, 20, 24)
    tovr.draw_items(w_bkg_img)

    w_bkg_img.save('out.png')


