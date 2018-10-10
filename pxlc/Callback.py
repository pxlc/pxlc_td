
class Callback(object):

    def __init__(self, callback_fn, callback_data):

        self.callback_fn = callback_fn
        self.cb_data = callback_data

    def wrapper_fn(self, *argv):
        print(':: hello from Callback.wrapper_fn()')
        self.callback_fn( self.cb_data, argv )

