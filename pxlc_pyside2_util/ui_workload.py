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

The UiWorkLoadManager class included here provides a convenient utility
for executing a long running task in another thread, while being able to
communicate progress and updates back to your PySide2 GUI.
'''

import sys
import traceback

from typing import (
    Callable,
    Optional,
)

from PySide2.QtCore import (
    QRunnable,
    QObject,
    QThreadPool,
    Signal,
    Slot,
)


class _UiWorkLoadSignals(QObject):

    finished = Signal()
    error = Signal(dict)     # status_data
    result = Signal(dict)    # status_data with result key
    progress = Signal(dict, float, str)  # progress amount and progress message


class _UiWorkLoad(QRunnable):

    def __init__(self, work_fn: Callable, work_data: dict):

        super().__init__()

        self.work_fn = work_fn
        self.work_data = work_data
        self.status_data = {'status': 'NOT_STARTED'}

        self.signals = _UiWorkLoadSignals()

    def update_progress(self, update_data: dict,
                        progress_percent: Optional[float] = 0.0,
                        progress_message: Optional[str] = ''):

        self.signals.progress.emit(update_data, progress_percent,
                                   progress_message)

    @Slot()
    def run(self):

        try:
            self.status_data = {
                'status': 'RUNNING',
            }
            result = self.work_fn(self.work_data, self.update_progress)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.status_data.update({
                'status': 'ERROR',
                'exctype': exctype,
                'exc_value': value,
                'traceback_str': traceback.format_exc(),
            })
            self.signals.error.emit(self.status_data)
        else:
            self.status_data.update({
                'status': 'COMPLETED',
                'result': result,
            })
            self.signals.result.emit(self.status_data)
        finally:
            self.signals.finished.emit()


class UiWorkLoadManager(QObject):

    def __init__(self):

        super().__init__()

        self.threadpool = QThreadPool()
        self.workload_info_by_name = {}

    def add_workload(self, workload_name: str, work_fn: Callable,
                     finished_callback_fn: Callable,
                     error_callback_fn: Callable,
                     result_callback_fn: Callable,
                     progress_callback_fn: Callable):

        self.workload_info_by_name[workload_name] = {
            'work_fn': work_fn,
            'finished_fn': finished_callback_fn,
            'error_fn': error_callback_fn,
            'result_fn': result_callback_fn,
            'progress_fn': progress_callback_fn,
        }

    def run_workload(self, workload_name: str, workload_data: dict):

        workload_info = self.workload_info_by_name[workload_name]
        ui_workload = _UiWorkLoad(workload_info['work_fn'], workload_data)

        ui_workload.signals.finished.connect(workload_info['finished_fn'])
        ui_workload.signals.error.connect(workload_info['error_fn'])
        ui_workload.signals.result.connect(workload_info['result_fn'])
        ui_workload.signals.progress.connect(workload_info['progress_fn'])

        self.threadpool.start(ui_workload)


