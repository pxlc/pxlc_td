
import os

from PIL import Image, ImageDraw, ImageColor, ImageFont

PXLC_TD_ROOT = '/'.join(os.path.abspath(__file__).replace('\\','/').split('/')[:-3])


class TextOverlay(object):

    def __init__(self, fill_color_str, stroke_color_str='', stroke_pixel_width=1, ttf_filepath=''):

        self.fill_color_str = fill_color_str
        self.stroke_color_str = stroke_color_str
        self.stroke_pixel_width = stroke_pixel_width

        self.text_item_list = []

        if ttf_filepath:
            self.ttf_filepath = ttf_filepath
        else:
            self.ttf_filepath = '%s/res/font/DejaVuSansMono/DejaVuSansMono.ttf' % PXLC_TD_ROOT

    def add_text_item(self, text_message, x, y, font_size):

        self.text_item_list.append({'text': text_message, 'pos': (x, y), 'font_size': font_size})

    def _draw_text_message(self, draw_obj, x, y, text, font_size):

        font = ImageFont.truetype(self.ttf_filepath, size=font_size)

        if self.stroke_color_str is not None:
            stroke_thickness = self.stroke_pixel_width
            for st_y in range(0-stroke_thickness, stroke_thickness+1):
                for st_x in range(0-stroke_thickness, stroke_thickness+1):
                    draw_obj.text((x+st_x, y+st_y), text, font=font, fill=self.stroke_color_str)

        draw_obj.text((x, y), text, fill=self.fill_color_str, font=font)

    def draw_items(self, pil_img_to_draw_on):

        draw_obj = ImageDraw.Draw(pil_img_to_draw_on)
        for t_item in self.text_item_list:
            text = t_item.get('text')
            (x, y) = t_item.get('pos')
            f_size = t_item.get('font_size')
            self._draw_text_message(draw_obj, x, y, text, f_size)


def add_color_bkg_to_image( pil_img_w_alpha, bkg_rgba_int_tuple ):

    (w, h) = pil_img_w_alpha.size

    # NOTE: bkg_rgb_int_tuple example: (127, 127, 127, 255)
    bkg_color_img = Image.new('RGBA', (w, h), bkg_rgba_int_tuple)  # (width, height), (r, g, b, a)

    combined_img = Image.alpha_composite(bkg_color_img, pil_img_w_alpha)

    return combined_img


