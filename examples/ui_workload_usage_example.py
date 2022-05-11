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

'''
Requires Python 3.7+ and PySide2

This example script demonstrates the usage of the UiWorkLoadManager class of
the pxlc_pyside2_util package. This class provides a convenient utility
for executing a long running task in another thread, while being able to
communicate progress and updates back to your PySide2 GUI.
'''

import os
import sys
import time
import random

from typing import Callable

from PySide2.QtWidgets import (
    QApplication,
    QDialog,
    QVBoxLayout,
    QPushButton,
    QTextEdit,
    QProgressBar,
)

from PySide2.QtCore import (
    Qt,
    QRect,
)

__EXAMPLES_DIR__ = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
sys.path.append(f'{__EXAMPLES_DIR__}/..')

# pxlc imports
from pxlc_pyside2_util.ui_workload import UiWorkLoadManager


class AppDialog(QDialog):

    """GUI Application using PySide2 widgets"""
    def __init__(self, parent=None):

        super(AppDialog, self).__init__(parent=parent)

        self.setWindowTitle('UiWorkLoadManager Usage Example')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setGeometry(QRect(200, 200, 500, 500))

        self.ui_workload_manager = UiWorkLoadManager()
        self.ui_workload_manager.add_workload(
            'My Work', self.workload_test,
            self.finished_callback,
            self.error_callback,
            self.result_callback,
            self.progress_callback
        )

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.startbutton = QPushButton('START')
        self.startbutton.clicked.connect(self.run)
        layout.addWidget(self.startbutton)

        self.stopbutton = QPushButton('STOP')
        self.stopbutton.clicked.connect(self.stop)
        layout.addWidget(self.stopbutton)

        self.progressbar = QProgressBar(self)
        self.progressbar.setRange(0, 100)
        layout.addWidget(self.progressbar)

        self.info = QTextEdit(self)
        self.info.append('Hello')
        layout.addWidget(self.info)

        self.current_progress = 0
        return

    def run(self):
        """call process"""

        self.stopped = False
        self.workload_data = {}
        self.ui_workload_manager.run_workload('My Work', self.workload_data)

    def stop(self):
        self.stopped=True

    def finished_callback(self):
        if self.current_progress < 100:
            self.info.append('Task not fully completed, reaching {}%'.format(self.current_progress))
        else:
            self.info.append('Task completed fully, to 100%')

    def error_callback(self, status_d: dict):
        self.info.append('ERROR!')
        self.info.append(status_d.get('traceback_str'))

    def result_callback(self, status_d: dict):
        self.info.append(status_d.get('status'))
        self.info.append(f' ... RESULT is: {status_d.get("result")}')

    def progress_callback(self, update_data: dict, progress_percent: float, progress_message: str):
        """Update progress"""

        percent_as_int = int(progress_percent + 0.5)
        random_int_value = update_data.get('random_int_value', -1)

        self.current_progress = percent_as_int

        self.progressbar.setValue(percent_as_int)
        self.info.append('random value: %s' % random_int_value)        

    def workload_test(self, workdata: dict, update_progress_fn: Callable):
        """Do some process here"""

        total = 500
        for i in range(0,total):
            time.sleep(0.05)
            x = random.randint(1,1e4)
            progress_percent = (float(i+1) / float(total)) * 100.0
            if progress_percent > 100.0:
                progress_percent = 100.0
            update_progress_fn({'random_int_value': x}, progress_percent=progress_percent,
                               progress_message='')
            if self.stopped == True:
                return 'User Stopped Processing!'

        return 'Entire workload completed!'


if __name__ == '__main__':

    app = QApplication([])

    app_dialog = AppDialog()
    app_dialog.show()

    sys.exit(app.exec_())


