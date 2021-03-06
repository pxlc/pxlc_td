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

import getopt
import types

#
# opt definition ...
#
#     { 'short': 'h', 'long': 'help', 'type': [None | bool | str | int | etc.], 'dest': 'help_flag',
#         'allowed': [ ... ], 'not_allowed': [ ... ] }
#

class MainOptParse( object ):

    def __init__( self, opt_defn_list=[] ):

        self.opt_key_list = []
        self.opt_info_by_key = {}

        self.script = None


    def add_opt( self, short_name, long_name, help_str, dest=None, opt_type=None, default_value=None,
                 allowed=[], not_allowed=[] ):

        opt_info = {}

        if short_name:
            if len(short_name) > 1:
                raise Exception('Short name "{}" invalid -- MUST be a single character.'.format( short_name ))
            opt_info['short'] = short_name
        if long_name:
            opt_info['long'] = long_name

        opt_info['help'] = help_str
        if default_value is not None:
            opt_info['default'] = default_value

        opt_key = short_name
        if long_name:
            opt_key = long_name
        if dest:
            opt_key = dest
        if not opt_key:
            raise Exception('No destination opt key, long, or short name provided.')

        opt_info['value'] = None
        opt_info['type'] = opt_type  # Note that value here of None means simple flag, no value
        if not opt_type:
            opt_info['value'] = False

        if allowed:
            opt_info['allowed'] = allowed[ : ]
        if not_allowed:
            opt_info['not_allowed'] = not_allowed[ : ]

        self.opt_info_by_key[ opt_key ] = opt_info.copy()
        self.opt_key_list.append( opt_key )


    def get_opt_value( self, opt_key ):

        opt_info = self.opt_info_by_key.get( opt_key )
        if opt_info:
            value = opt_info.get('value')
            default = opt_info.get('default')
            if value is None:
                return default
            return value
        return None


    def print_opt_values( self ):

        print('')
        print('===[ Options ]===')
        print('')

        for opt_key in self.opt_key_list:
            opt_value = self.get_opt_value( opt_key )
            print('')
            if type(opt_value) in types.StringTypes:
                print(' :: {} = "{}"'.format( opt_key, opt_value ))
            else:
                print(' :: {} = {}'.format( opt_key, opt_value ))

        print('')
        print('')


    def print_opt_info( self ):

        print('')
        print('===[ Options ]===')
        print('')

        for opt_key in self.opt_key_list:
            opt_info = self.opt_info_by_key.get( opt_key )
            if not opt_info:
                continue
            print('')
            print(' :: {} => {}'.format( opt_key, opt_info ))

        print('')
        print('')


    def usage( self ):

        print('')
        print('  Usage: python {} [OPTIONS] '.format(self.script))
        print('')
        print('  ---[ OPTIONS ]---')
        for opt_key in self.opt_key_list:
            opt_info = self.opt_info_by_key.get( opt_key )
            if not opt_info:
                continue
            o_type = opt_info.get('type')
            if not o_type:
                o_type = 'flag'
            o_default = opt_info.get('default')
            o_value = self.get_opt_value(opt_key)
            o_short = opt_info.get('short')
            o_long = opt_info.get('long')
            o_help = opt_info.get('help')
            usage_arr = ['  ']
            if o_short:
                usage_arr.append('-{}'.format(o_short))
                if o_type != 'flag':
                    usage_arr.append('<{}>'.format(o_long.upper().replace('-','_')))
                if o_long:
                    usage_arr.append('|')
            if o_long:
                usage_arr.append('--{}'.format(o_long))
                if o_type != 'flag':
                    usage_arr.append('<{}>'.format(o_long.upper().replace('-','_')))
            usage_arr.append('...')
            usage_arr.append(o_help)
            print('')
            print(' '.join(usage_arr))

        print('')

        print(' *** USAGE!')


    def _setup_for_parse( self ):

        self.short_opt_str = ''
        self.long_opt_list = []

        self.opt_key_by_short = {}
        self.opt_key_by_long = {}

        for opt_key in self.opt_key_list:
            opt_info = self.opt_info_by_key.get( opt_key )
            if not opt_info:
                continue
            opt_type = opt_info.get('type')
            short_name = opt_info.get('short')
            if short_name:
                if opt_type:
                    self.short_opt_str += '{}:'.format( short_name )
                else:
                    # if the opt type is None, then it is a straight flag, assuming value False except when flag is
                    # present on command line then value will become True
                    #
                    self.short_opt_str += short_name
                self.opt_key_by_short[ short_name ] = opt_key
            long_name = opt_info.get('long')
            if long_name:
                if opt_type:
                    self.long_opt_list.append( '{}='.format( long_name ) )
                else:
                    self.long_opt_list.append( long_name )
                self.opt_key_by_long[ long_name ] = opt_key


    def parse( self, full_sys_args ):

        self._setup_for_parse()

        self.script = os.path.basename( full_sys_args[0] )
        raw_arg_list = full_sys_args[ 1 : ]

        value_error_list = []

        try:
            opt_pair_list, arg_list = getopt.getopt( raw_arg_list, self.short_opt_str, self.long_opt_list )
        except getopt.GetoptError as err:
            print( str(err) )
            usage()
            sys.exit( 2 )

        for opt_flag, opt_value in opt_pair_list:
            opt_key = None
            opt_flag_short = opt_flag[ 1 : ]
            opt_flag_long = opt_flag[ 2 : ]

            if opt_flag_short in self.opt_key_by_short:
                opt_key = self.opt_key_by_short.get( opt_flag_short )
            elif opt_flag_long in self.opt_key_by_long:
                opt_key = self.opt_key_by_long.get( opt_flag_long )

            if not opt_key:
                continue  # TODO: raise Exception here? We really should not get here

            opt_info = self.opt_info_by_key.get( opt_key )
            if not opt_info:
                continue  # TODO: raise Exception here? We really should not get here

            if not opt_info.get('type'):  # this means its a straight flag, existence on command line means value True
                opt_info['value'] = True
                continue

            try:
                value = ( opt_info.get('type') )( opt_value )
                opt_info['value'] = value
            except ValueError as err:
                value_error_list.append( 'For option key "{}", got {}'.format( opt_key, str(err) ) )

        if value_error_list:
            print('')
            for v_err in value_error_list:
                print( '  ValueError: {}'.format( v_err ) )
            print('')
            self.usage()
            sys.exit( 2 )

        return True


if __name__ == '__main__':

    mop = MainOptParse()

    mop.add_opt( 'v', 'verbose', 'flag to run in verbose mode.' )
    mop.add_opt( 'p', 'path', 'specify a path to use.', opt_type=str )
    mop.add_opt( 'i', 'integer-num', 'provide an integer value to use.', opt_type=int )
    mop.add_opt( 'f', 'float-num', 'provide an float value to use.', opt_type=float )

    mop.parse( sys.argv )
    # mop.print_opt_info()
    mop.print_opt_values()


