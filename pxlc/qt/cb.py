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

from .. import Callback

_g_pxlc_callbacks = []

def connect_callback(wdg_signal, callback_fn, cb_data, containing_obj=None):

    global _g_pxlc_callbacks

    callback = Callback.Callback(callback_fn, cb_data)
    wdg_signal.connect(callback.wrapper_fn)

    if containing_obj:
        if isinstance(containing_obj, object):
            if not hasattr(containing_obj, '_pxlc_callbacks'):
                containing_obj._pxlc_callbacks = []
            containing_obj._pxlc_callbacks.append(callback)
    else:
        _g_pxlc_callbacks.append(callback)


