
import json
import sys

from PySide import QtGui, QtCore


class EasyDataTableWdg(QtGui.QTableWidget):

    def __init__(self, context, col_config, column_order, data_rows, parent=None):

        super(EasyDataTableWdg, self).__init__(parent=parent)

        self.context = context
        self.col_config = col_config    # col_config will have callbacks for cell clicks?
        self.column_order = column_order
        self.data_rows = data_rows
        self.wdg_by_row_col = {}

        self.build_table()

    def get_col_idx_by_col_name(self, col_name):
        return self.column_order.index(col_name)

    def get_column_order(self):
        return self.column_order

    def get_data_rows(self):
        return self.data_rows

    def get_widget_by_row_col(self, row_idx, col_idx):
        return self.wdg_by_row_col.get((row_idx, col_idx ))

    def build_table(self):

        self.wdg_by_row_col = {}

        self.setRowCount(len(self.data_rows))
        self.setColumnCount(len(self.column_order))

        for r_idx, row_data in enumerate(self.data_rows):
            for c_idx, col_name in enumerate(self.column_order):
                wdg = None
                get_widget_fn = self.col_config.get(col_name, {}).get('widget_fn')
                is_editable = self.col_config.get(col_name, {}).get('is_editable', True)
                if get_widget_fn:
                    wdg = get_widget_fn(self, r_idx, col_name, self.col_config.get(col_name, {}), self.context)
                if wdg:
                    if not is_editable:
                        wdg.setEnabled(False)
                    self.setCellWidget(r_idx, c_idx, wdg)
                    print('  (%s, %s) => %s' % (r_idx, c_idx, type(self.item(r_idx, c_idx))))
                    self.wdg_by_row_col[ (r_idx, c_idx) ] = wdg
                    continue
                twdg_item = QtGui.QTableWidgetItem('{}'.format(row_data.get(col_name)))
                if not is_editable:
                    twdg_item.setFlags(twdg_item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.setItem(r_idx, c_idx, twdg_item)
                print('  (%s, %s) => %s' % (r_idx, c_idx, type(self.item(r_idx, c_idx))))

        header_labels = []
        for col_name in self.column_order:
            col_header = ' '.join([ word.capitalize() for word in col_name.replace('_',' ').split() ])
            cfg_header = self.col_config.get(col_name, {}).get('header_label')
            if cfg_header:
                col_header = cfg_header
            header_labels.append(col_header)

        self.setHorizontalHeaderLabels(header_labels)


def checkbox_callback(data_str):

    import _ctypes

    bits = data_str.split('|')
    row_idx = int(bits[0])
    col_name = bits[1]
    easy_table_id = long(bits[2])
    checkbox_wdg_id = long(bits[3])

    easy_table = _ctypes.PyObj_FromPtr(easy_table_id)
    data_rows = easy_table.get_data_rows()
    col_idx = easy_table.get_col_idx_by_col_name(col_name)

    checkbox_wdg = _ctypes.PyObj_FromPtr(checkbox_wdg_id)

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
    # stmt = 'wdg.stateChanged.connect(lambda:checkbox_callback("{ri}|{cn}|{dr_id}|{w_id}"))'.format(
    stmt = 'wdg.clicked.connect(lambda:checkbox_callback("{ri}|{cn}|{etw_id}|{w_id}"))'.format(
            ri=row_idx, cn=col_name, etw_id=id(easy_table_wdg), w_id=id(wdg))
    exec(stmt)
    return wdg


def main2():  
    app = QtGui.QApplication(sys.argv)

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

    table = EasyDataTableWdg({}, col_config, columns, data_list)

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
