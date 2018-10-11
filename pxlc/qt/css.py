# -------------------------------------------------------------------------------
# MIT License
#
# Copyright (c) 2018 pxlc@github
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
# -------------------------------------------------------------------------------

def wdg_add_classes( q_wdg, css_classes_str ):

    css_class_list = css_class_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'on')


def wdg_remove_classes( q_wdg, css_classes_str ):

    css_class_list = css_classes_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'off')


def wdg_set_classes( q_wdg, css_classes_str ):

    for prop_name in q_wdg.dynamicPropertyNames():
        # NOTE: prop_name needs to be cast to str for .setProperty() and value None will remove property
        q_wdg.setProperty(str(prop_name), None)

    css_class_list = css_classes_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'on')


