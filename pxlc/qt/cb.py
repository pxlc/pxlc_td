
# from PySide import QtGui, QtCore

from .. import Callback

def connect_callback(wdg_signal, callback_fn, cb_data):

    callback = Callback.Callback(callback_fn, cb_data)
    wdg_signal.connect(lambda:callback.wrapper_fn(callback))

