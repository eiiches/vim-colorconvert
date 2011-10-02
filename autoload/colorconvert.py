# colorconvert.vim
# Author: Eiichi Sato <sato.eiichi@gmail.com>
# Last Modified: 2 Oct 2011
# License: MIT license
#     Permission is hereby granted, free of charge, to any person obtaining
#     a copy of this software and associated documentation files (the
#     "Software"), to deal in the Software without restriction, including
#     without limitation the rights to use, copy, modify, merge, publish,
#     distribute, sublicense, and/or sell copies of the Software, and to
#     permit persons to whom the Software is furnished to do so, subject to
#     the following conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import functools
import vim

class ColorConvert(object):
    class ColorTable: # {{{
        class GnomeTerminal: # {{{
            class Tango: # {{{
                basic = [[0x00, 0x00, 0x00], [0xCC, 0x00, 0x00],
                         [0x4E, 0x9A, 0x06], [0xC4, 0xA0, 0x00],
                         [0x34, 0x65, 0xA5], [0x75, 0x50, 0x7B],
                         [0x06, 0x98, 0x9A], [0xD3, 0xD7, 0xCF],
                         [0x55, 0x57, 0x53], [0xEF, 0x29, 0x29],
                         [0x8A, 0xE2, 0x34], [0xFC, 0xE9, 0x4F],
                         [0x72, 0x9F, 0xCF], [0xAD, 0x7F, 0xA8],
                         [0x34, 0xE2, 0xE2], [0xEE, 0xEE, 0xEC]]
                values = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
            # }}}
            class Linux: # {{{
                basic = [[0x00, 0x00, 0x00], [0xAA, 0x00, 0x00],
                         [0x00, 0xAA, 0x00], [0xAA, 0x55, 0x00],
                         [0x00, 0x00, 0xAA], [0xAA, 0x00, 0xAA],
                         [0x00, 0xAA, 0xAA], [0xAA, 0xAA, 0xAA],
                         [0x55, 0x55, 0x55], [0xFF, 0x55, 0x55],
                         [0x55, 0xFF, 0x55], [0xFF, 0xFF, 0x55],
                         [0x55, 0x55, 0xFF], [0xFF, 0x55, 0xFF],
                         [0x55, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF]]
                values = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
            # }}}
        # }}}
        class XTerm: # {{{
            basic = [[0x00, 0x00, 0x00], [0xCD, 0x00, 0x00],
                     [0x00, 0xCD, 0x00], [0xCD, 0xCD, 0x00],
                     [0x00, 0x00, 0xEE], [0xCD, 0x00, 0xCD],
                     [0x00, 0xCD, 0xCD], [0xE5, 0xE5, 0xE5],
                     [0x7F, 0x7F, 0x7F], [0xFF, 0x00, 0x00],
                     [0x00, 0xFF, 0x00], [0xFF, 0xFF, 0x00],
                     [0x5C, 0x5C, 0xFF], [0xFF, 0x00, 0xFF],
                     [0x00, 0xFF, 0xFF], [0xFF, 0xFF, 0xFF]]
            values = [0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF]
        # }}}
    # }}}
    class memoized(object): # {{{
        def __init__(self, func):
            self.func = func
            self.cache = {}
        def __call__(self, *args):
            try:
                return self.cache[args]
            except KeyError:
                value = self.func(*args)
                self.cache[args] = value
                return value
            except TypeError:
                return self.func(*args)
        def __get__(self, obj, objtype):
            return functools.partial(self.__call__, obj)
    # }}}
    # {{{ vim glue

    def vim_cterm_to_gui(self, cterm):
        vim.command('return "{0}"'.format(self.cterm_to_gui(cterm)))

    def vim_gui_to_cterm(self, gui):
        vim.command('return "{0}"'.format(self.gui_to_cterm(gui)))

    def vim_cterm_to_rgb(self, cterm):
        vim.command('return [{0},{1},{2}]'.format(*self.cterm_to_rgb(cterm)))

    def vim_gui_to_rgb(self, gui):
        vim.command('return [{0},{1},{2}]'.format(*self.gui_to_rgb(gui)))

    def vim_rgb_to_cterm(self, rgb):
        vim.command('return "{0}"'.format(self.rgb_to_index(rgb)))

    def vim_rgb_to_gui(self, rgb):
        vim.command('return "{0}"'.format(self.rgb_to_code(rgb)))

    # }}}

    def __init__(self, colortable):
        self.colortable = eval('self.ColorTable.' + colortable)
        self.tmp_colors = list(enumerate(map(self.index_to_rgb, range(254))))

    @classmethod
    def code_to_rgb(klass, code):
        if code.startswith('#'):
            code = code[1:]
        if len(code) == 6:
            return int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16)
        elif len(code) == 3:
            return int(code[0]*2, 16), int(code[1]*2, 16), int(code[2]*2, 16)

    @classmethod
    def rgb_to_code(klass, rgb):
        values = map(lambda x: max(min(x, 255), 0), rgb)
        return '#{0:02X}{1:02X}{2:02X}'.format(*values)

    def index_to_rgb(self, index):
        if index < 16:
            return self.colortable.basic[index]
        elif 16 <= index < 232:
            index -= 16
            return [self.colortable.values[(index//36)%6],
                    self.colortable.values[(index//6)%6],
                    self.colortable.values[index%6]]
        elif 232 <= index < 256:
            return [8+(index-232)*10]*3

    @memoized
    def rgb_to_index(self, rgb):
        def diff(color):
            r = color[1][0]-rgb[0]
            g = color[1][1]-rgb[1]
            b = color[1][2]-rgb[2]
            return r*r + g*g + b*b
        best = min((color for color in self.tmp_colors), key=diff)
        return best[0]

    def cterm_to_gui(self, cterm):
        try: rgb = self.index_to_rgb(int(cterm))
        except ValueError: # colornames like 'red' or 'blue'
            return cterm
        return self.rgb_to_code(rgb)

    def gui_to_cterm(self, gui):
        try: rgb = self.code_to_rgb(gui)
        except ValueError: # colornames like 'red' or 'blue'
            return gui
        return self.rgb_to_index(rgb)

    def cterm_colorname_to_index(self, colorname):
        # TODO : add more colors
        colornames = [
            'black', 'darkred', 'darkgreen', 'brown', 'darkblue', 'darkmagenta', 'darkcyan', 'lightgray',
            'darkgray', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        ]
        return colornames.index(colorname.lower())

    def gui_colorname_to_rgb(self, colorname):
        # FIXME
        return self.index_to_rgb(self.cterm_colorname_to_index(colorname))

    def cterm_to_rgb(self, cterm):
        try: rgb = self.index_to_rgb(int(cterm))
        except ValueError: # handle colornames
            rgb = self.index_to_rgb(self.cterm_colorname_to_index(cterm))
        return rgb

    def gui_to_rgb(self, gui):
        try: rgb = self.code_to_rgb(gui)
        except ValueError: # handle colornames
            rgb = self.gui_colorname_to_rgb(gui)
        return rgb

# vim: fdm=marker:fmr={{{,}}}
