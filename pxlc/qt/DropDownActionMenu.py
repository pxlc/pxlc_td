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

from PySide import QtCore, QtGui

from .. import Callback  # local package import

__INFO__ = '''

   item list:

    [
        {
            'label': 'Menu label',
            # ... and whatever else you want as data
        }
    ]

'''

class DropDownActionMenu(QtGui.QToolButton):

    def __init__(self, item_list, item_selected_cb_fn, button_label='', button_icon_path='',
                 use_arrow_icon=False, parent=None):

        super(DropDownActionMenu, self).__init__(parent=parent)

        if button_label:
            self.setText(button_label)

        if use_arrow_icon:
            self.setPopupMode(QtGui.QToolButton.MenuButtonPopup)
        else:
            self.setPopupMode(QtGui.QToolButton.InstantPopup)
            self.setStyleSheet('::menu-indicator{ width: 0px; }')  # this works!

        self.item_selected_cb_fn = item_selected_cb_fn
        self._toolbutton_menu = QtGui.QMenu()

        self._callback_list = []
        self._load_items(item_list)

        self.setMenu(self._toolbutton_menu)

    def _load_items(self, item_list):

        self.item_list = item_list[:]

        for item in self.item_list:
            cb = Callback.Callback(self.central_cb_fn, item)
            self._callback_list.append(cb)
            self._toolbutton_menu.addAction(item.get('label',''), cb.wrapper_fn)

    def central_cb_fn(self, item, args):

        self.item_selected_cb_fn(item)


