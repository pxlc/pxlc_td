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

import os
import sys
import json

from PySide import QtGui, QtCore

_path_to_add = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(_path_to_add)

import pxlc


def ensure_only_single_active_checked(cb_data, args):

    row_idx = cb_data.get('row_idx')
    col_name = cb_data.get('col_name')
    easy_table = cb_data.get('easy_table_wdg')
    checkbox_wdg = cb_data.get('wdg')

    data_rows = easy_table.get_data_rows()
    col_idx = easy_table.get_col_idx_by_col_name(col_name)

    is_checked = checkbox_wdg.isChecked()
    print('')
    print(':: col_name is "{}", checked? {}'.format(col_name, is_checked))
    data_rows[row_idx][col_name] = is_checked
    print('')
    print(json.dumps(data_rows[row_idx], indent=4, sort_keys=True))
    print('')

    if is_checked:
        for r_idx, row in enumerate(data_rows):
            if r_idx == row_idx:
                continue
            wdg = easy_table.get_widget_by_row_col(r_idx, col_idx)
            if wdg and type(wdg) is QtGui.QCheckBox:
                wdg.setChecked(False)


class MainExampleWdg(QtGui.QWidget):  

    def __init__(self):

        super(MainExampleWdg, self).__init__()

        columns = ['greeting', 'language', 'activate']
        data_list = [
            {'greeting': 'Hello', 'language': 'English', 'activate': False},
            {'greeting': 'Bonjour', 'language': 'French', 'activate': True},
            {'greeting': 'Ciao', 'language': 'Italian', 'activate': False},
            {'greeting': 'Ohaiyo', 'language': 'Japanese', 'activate': True},
        ]

        col_config = {
            'greeting': {
            },
            'language': {
                'is_editable': False
            },
            'activate': {
                'widget_type': 'check_box',
                'edit_response_fn': ensure_only_single_active_checked
            },
        }

        #DEBUG
        print('')
        print('-------[ QStyleFactory styles ]----------')
        print('')
        for k in QtGui.QStyleFactory.keys():
            print('    %s' % k)
        print('')
        print('-----------------------------------------')
        print('')
        #DEBUG

        q_style = None
        style_name = "Plastique"
        if style_name in [ str(k) for k in QtGui.QStyleFactory.keys() ]:
            q_style = QtGui.QStyleFactory.create(style_name)
        else:
            print('')
            print(':: Style name "%s" not found in QStyleFactory ... ignoring style.' % style_name)
            print('')

        if q_style:
            self.setStyle(q_style)

        self.main_vbox = QtGui.QVBoxLayout()
        self.setLayout(self.main_vbox)

        self.title_hbox = QtGui.QHBoxLayout()
        self.main_vbox.addLayout(self.title_hbox)

        self.title_label = QtGui.QLabel()
        self.title_label.setText("Example of EasyDataTableWdg class   ")

        self.action_menu = pxlc.qt.DropDownActionMenu([
                {'label': 'Print Selected', 'data_str': 'Hello One!'},
                {'label': 'two', 'data_str': 'Hello Two!'},
                {'label': 'three', 'data_str': 'Hello Three!'},
            ],
            self.action_menu_callback, button_label='Actions')

        self.title_hbox.addWidget(self.title_label)
        self.title_hbox.addWidget(self.action_menu)
        self.title_hbox.addStretch()

        self.table = pxlc.qt.EasyDataTableWdg({}, col_config, columns, data_list)

        self.main_vbox.addWidget(self.table)

    def action_menu_callback(self, item):

        print(':: got action with data_str value of "%s"' % item.get('data_str'))

        if item.get('label') == 'Print Selected':
            pass


def main2():  

    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet('''
QTableView
{
    color: #AAAAAA;
    border: 1px solid #000000;
    background: #888888;
    gridline-color: #444444;
}
QTableView::item
{
    background: #666666;
}
QHeaderView::section
{
    spacing: 10px;
    background-color: #FFFF88;
    color: blue;
    border: 1px solid red;
    margin: 1px;
    text-align: right;
    font-family: arial;
    font-size:12px;
}
    ''')

    example_win = MainExampleWdg()

    example_win.setWindowTitle("QTableWidget Example")
    example_win.resize(400, 250)
    example_win.show()

    return app.exec_()


def main():  
    app 	= QtGui.QApplication(sys.argv)
    table 	= QtGui.QTableWidget()
    tableItem 	= QtGui.QTableWidgetItem()

    column_order = ['one', 'two', 'three', 'four']

    data_rows = [
        {'one': 1, 'two': 2, 'three': 3, 'four': 4},
        {'one': 11, 'two': 22, 'three': 33, 'four': 44},
        {'one': 111, 'two': 222, 'three': 333, 'four': 444},
    ]
 
    # initiate table
    table.setWindowTitle("QTableWidget Example")
    table.resize(400, 250)
    table.setRowCount(len(data_rows))
    table.setColumnCount(len(column_order))
 
    for r_idx, dr in enumerate(data_rows):
        for c_idx, col in enumerate(column_order):
            table.setItem(r_idx, c_idx, QtGui.QTableWidgetItem("%s" % dr.get(col)))
    # set data
    __REF__ = '''
    table.setItem(0,0, QtGui.QTableWidgetItem("Item (1,1)"))
    table.setItem(0,1, QtGui.QTableWidgetItem("Item (1,2)"))
    table.setItem(1,0, QtGui.QTableWidgetItem("Item (2,1)"))
    table.setItem(1,1, QtGui.QTableWidgetItem("Item (2,2)"))
    table.setItem(2,0, QtGui.QTableWidgetItem("Item (3,1)"))
    table.setItem(2,1, QtGui.QTableWidgetItem("Item (3,2)"))
    table.setItem(3,0, QtGui.QTableWidgetItem("Item (4,1)"))
    table.setItem(3,1, QtGui.QTableWidgetItem("Item (4,2)"))
    '''
 
    # show table
    table.setHorizontalHeaderLabels( [ c.capitalize() for c in column_order ] )
    table.show()
    return app.exec_()
 

if __name__ == '__main__':
    main2()

