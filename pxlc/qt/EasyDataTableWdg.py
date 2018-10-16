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

import json
import sys

from PySide import QtGui, QtCore

from .cb import connect_callback


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

    def _edit_cb_check_box(self, cb_data, args):

        row_idx = cb_data.get('row_idx')
        col_name = cb_data.get('col_name')
        wdg = cb_data.get('wdg')
        self.get_data_rows()[row_idx][col_name] = wdg.isChecked()

        edit_response_fn = cb_data.get('edit_response_fn')
        if edit_response_fn:
            edit_response_fn(cb_data, args)

    def _edit_cb_line_edit(self, cb_data, args):

        row_idx = cb_data.get('row_idx')
        col_name = cb_data.get('col_name')
        wdg = cb_data.get('wdg')

        if self.get_data_rows()[row_idx][col_name] != str(wdg.text()):
            self.get_data_rows()[row_idx][col_name] = str(wdg.text())
            print('')
            print(json.dumps(self.get_data_rows()[row_idx], indent=4, sort_keys=True))
            print('')

        edit_response_fn = cb_data.get('edit_response_fn')
        if edit_response_fn:
            edit_response_fn(cb_data, args)

    def _create_wdg_by_type(self, wdg_type, row_idx, col_name, col_cfg_d):

        if wdg_type == 'check_box':
            wdg = QtGui.QCheckBox()
            if self.get_data_rows()[row_idx].get(col_name):
                wdg.setChecked(True)
            else:
                wdg.setChecked(False)
            cb_data = {
                'row_idx': row_idx, 'col_name': col_name, 'easy_table_wdg': self, 'wdg_type': wdg_type,
                'edit_response_fn': col_cfg_d.get('edit_response_fn'), 'wdg': wdg,
            }
            connect_callback(wdg.stateChanged, self._edit_cb_check_box, cb_data)
            return wdg

        elif wdg_type == 'line_edit':
            wdg = QtGui.QLineEdit()
            value = self.get_data_rows()[row_idx].get(col_name)
            print(':: "%s" column value is "%s" (type %s)' % (col_name, value, type(value)))
            if not value:
                value = ''
            wdg.setText(value)
            cb_data = {
                'row_idx': row_idx, 'col_name': col_name, 'easy_table_wdg': self, 'wdg_type': wdg_type,
                'edit_response_fn': col_cfg_d.get('edit_response_fn'), 'wdg': wdg,
            }
            # connect_callback(wdg.textChanged, self._edit_cb_line_edit, cb_data) # this fires every character
            connect_callback(wdg.editingFinished, self._edit_cb_line_edit, cb_data)
            return wdg

        return None

    def build_table(self):

        self.wdg_by_row_col = {}

        self.setRowCount(len(self.data_rows))
        self.setColumnCount(len(self.column_order))

        for r_idx, row_data in enumerate(self.data_rows):
            for c_idx, col_name in enumerate(self.column_order):
                col_cfg_d = self.col_config.get(col_name, {})

                col_wdg_type = col_cfg_d.get('widget_type')
                is_editable = col_cfg_d.get('is_editable', True)

                wdg = self._create_wdg_by_type(col_wdg_type, r_idx, col_name, col_cfg_d)

                if wdg:
                    if not is_editable:
                        wdg.setEnabled(False)
                    self.setCellWidget(r_idx, c_idx, wdg)
                    self.wdg_by_row_col[ (r_idx, c_idx) ] = wdg
                    continue

                # --- otherwise default to using QTableWidgetItem for text editing
                twdg_item = QtGui.QTableWidgetItem('{}'.format(row_data.get(col_name)))
                if not is_editable:
                    twdg_item.setFlags(twdg_item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.setItem(r_idx, c_idx, twdg_item)

        header_labels = []
        for col_name in self.column_order:
            col_header = ' '.join([ word.capitalize() for word in col_name.replace('_',' ').split() ])
            cfg_header = self.col_config.get(col_name, {}).get('header_label')
            if cfg_header:
                col_header = cfg_header
            header_labels.append(col_header)

        self.setHorizontalHeaderLabels(header_labels)

        connect_callback(self.cellChanged, self._edit_cb_cell_changed, {'signal_name': 'cellChanged'}, self)

        # --- For testing, uncomment lines below:
        # connect_callback(self.cellActivated, self._test_signal, {'signal_name': 'cellActivated'}, self)
        # connect_callback(self.cellClicked, self._test_signal, {'signal_name': 'cellClicked'}, self)
        # connect_callback(self.cellDoubleClicked, self._test_signal, {'signal_name': 'cellDoubleClicked'}, self)
        # connect_callback(self.cellPressed, self._test_signal, {'signal_name': 'cellPressed'}, self)
        self.setMouseTracking(True)  # must be on for "cellEntered" signal to fire
        connect_callback(self.cellEntered, self._test_signal, {'signal_name': 'cellEntered'}, self)

        h_hdr = self.horizontalHeader()
        h_hdr.setResizeMode(QtGui.QHeaderView.Stretch)
        for idx in range(len(self.column_order)):
            connect_callback(h_hdr.sectionEntered, self._test_signal,
                             {'signal_name': 'sectionEntered', 'idx': idx}, self)

        v_hdr = self.verticalHeader()
        v_hdr.setResizeMode(QtGui.QHeaderView.Stretch)

        pass

    def _edit_cb_cell_changed(self, cb_data, args):

        row_idx = args[0]
        col_idx = args[1]

        col_name = self.column_order[col_idx]
        item = self.item(row_idx, col_idx)

        prev_value = self.get_data_rows()[row_idx][col_name]
        new_value = str(item.text())

        if prev_value != new_value:
            self.get_data_rows()[row_idx][col_name] = new_value
            # print('')
            # print('[SIGNAL]: "cellChanged" - cell (%s, %s) data changed from "%s" to "%s"' %
            #         (row_idx, col_idx, prev_value, new_value))
            # print('')
            pass

        col_cfg_d = self.col_config.get(col_name, {})
        pass_along_cb_data = {
            'row_idx': row_idx, 'col_name': col_name, 'easy_table_wdg': self, 'wdg_type': 'table_item',
            'edit_response_fn': col_cfg_d.get('edit_response_fn'), 'wdg': item,
        }
        edit_response_fn = pass_along_cb_data.get('edit_response_fn')
        if edit_response_fn:
            edit_response_fn(pass_along_cb_data, [row_idx, col_idx])

    def _test_signal2(self, x, y):

        print('[SIGNAL]: got (x,y) of (%s, %s)' % (x, y))

    def _test_signal(self, cb_data, args):

        if 'idx' in cb_data:
            print('[SIGNAL]: "%s" (idx=%s), args = %s' % (cb_data.get('signal_name'),
                                                            cb_data.get('idx'), list(args)))
        else:
            print('[SIGNAL]: "%s", args = %s' % (cb_data.get('signal_name'), list(args)))

    def leaveEvent(self, event):

        print('>> The Mouse has left the bulding!')

