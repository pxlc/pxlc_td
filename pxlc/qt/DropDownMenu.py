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

from .cb import connect_callback  # local import

__INFO__ = '''

   item list:

    [
        {
            'label': 'Menu label',
            'select_data': 'any type, returned if item is selected',
            'style': 'style sheet string (optional)',
        }
    ]

'''


class DropDownMenu(QtGui.QComboBox):

    def __init__(self, item_list=[], parent=None):

        super(DropDownMenu, self).__init__(parent=parent)

        self.item_list = item_list[:]

    def clear_all_items(self):

        while self.count() > 0:
            self.removeItem(0)

    def load_items(self, item_list):

        self.clear_all_items()
        self.item_list = item_list[:]

        for item in self.item_list:
            label = item.get('label','')
            self.addItem(label)

        self.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)

    def set_index_changed_callback(self, index_changed_cb_fn):

        connect_callback(self.currentIndexChanged, index_changed_cb_fn, {'wdg': self})

    def get_current_item(self):

        curr_idx = self.currentIndex()
        if curr_idx >= 0 and curr_idx < len(self.item_list):
            return self.item_list[curr_idx]
        return None

