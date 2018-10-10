
import json
import sys

from PySide import QtGui, QtCore

from .. import Callback


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


