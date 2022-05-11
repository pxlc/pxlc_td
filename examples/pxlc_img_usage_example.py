# ------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2022 pxlc@github
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ------------------------------------------------------------------------------

import os
import sys

PXLC_TD_ROOT = '/'.join(os.path.abspath(__file__).replace('\\','/').split('/')[:-2])

sys.path.append(PXLC_TD_ROOT)
import pxlc.img

from PIL import Image


if __name__ == '__main__':

    in_img = Image.open('%s/examples/data/rendered_frame.png' % PXLC_TD_ROOT)
    w_bkg_img = pxlc.img.add_color_bkg_to_image( in_img, (128, 128, 128, 255) )

    tovr = pxlc.img.TextOverlay('rgba(255, 255, 255, 255)', 'rgba(0, 0, 0, 255)', 1)

    tovr.add_text_item('Hello World!', 20, 20, 24)
    tovr.draw_items(w_bkg_img)

    w_bkg_img.save('out.png')


