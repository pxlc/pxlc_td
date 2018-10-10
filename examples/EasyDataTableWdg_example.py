
import os
import sys
import json

from PySide import QtGui, QtCore

_path_to_add = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(_path_to_add)

import pxlc


def checkbox_callback(cb_data, args):

    row_idx = cb_data.get('row_idx')
    col_name = cb_data.get('col_name')
    easy_table = cb_data.get('easy_table_wdg')
    checkbox_wdg = cb_data.get('checkbox_wdg')

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
            if row[col_name]:
                row[col_name] = False
                wdg = easy_table.get_widget_by_row_col(r_idx, col_idx)
                if wdg and type(wdg) is QtGui.QCheckBox:
                    wdg.setChecked(False)


def checkbox_widget(easy_table_wdg, row_idx, col_name, cfg_for_col, context):

    wdg = QtGui.QCheckBox()
    if easy_table_wdg.get_data_rows()[row_idx].get(col_name):
        wdg.setChecked(True)
    else:
        wdg.setChecked(False)

    cb_data = {
        'row_idx': row_idx,
        'col_name': col_name,
        'easy_table_wdg': easy_table_wdg,
        'checkbox_wdg': wdg,
    }

    pxlc.qt.connect_callback(wdg.clicked, checkbox_callback, cb_data)
    return wdg


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
            'widget_fn': checkbox_widget
        },
    }

    table = pxlc.qt.EasyDataTableWdg({}, col_config, columns, data_list)

    table.setWindowTitle("QTableWidget Example")
    table.resize(400, 250)

    table.show()
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

