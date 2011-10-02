" colorconvert.vim
" Author: Eiichi Sato <sato.eiichi@gmail.com>
" Last Modified: 2 Oct 2011
" License: MIT license
"   Permission is hereby granted, free of charge, to any person obtaining
"   a copy of this software and associated documentation files (the
"   "Software"), to deal in the Software without restriction, including
"   without limitation the rights to use, copy, modify, merge, publish,
"   distribute, sublicense, and/or sell copies of the Software, and to
"   permit persons to whom the Software is furnished to do so, subject to
"   the following conditions:
"
"   The above copyright notice and this permission notice shall be included
"   in all copies or substantial portions of the Software.
"
"   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
"   OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
"   MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
"   IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
"   CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
"   TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
"   SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

let s:cpo_save = &cpo
set cpo&vim

if !exists('g:colorconvert_profile')
	let g:colorconvert_profile = 'GnomeTerminal.Linux'
endif

function! colorconvert#initialize()
	" check python
	if has('python')
		let s:pyfile = 'pyfile'
		let s:python = 'python'
	elseif has('python3')
		let s:pyfile = 'py3file'
		let s:python = 'python3'
	else
		echoerr 'Python interface is not available.'
		finish
	endif

	" import module
	let pycode = globpath(&rtp, 'autoload/colorconvert.py')
	execute s:pyfile pycode

	" create converter instance
	let g:colorconvert_instance = 'colorconvert'
	execute s:python g:colorconvert_instance '=' 'ColorConvert("'.g:colorconvert_profile.'")'
endfunction
call colorconvert#initialize()

function! colorconvert#invoke(instance, method, ...)
	if a:0 > 0
		execute s:python a:instance.'.'.a:method.'(*'.string(a:000).')'
	else
		execute s:python a:instance.'.'.a:method.'()'
	endif
endfunction

function! colorconvert#cterm_to_gui(cterm)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_cterm_to_gui', a:cterm)
endfunction

function! colorconvert#gui_to_cterm(gui)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_gui_to_cterm', a:gui)
endfunction

function! colorconvert#cterm_to_rgb(cterm)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_cterm_to_rgb', a:cterm)
endfunction

function! colorconvert#gui_to_rgb(gui)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_gui_to_rgb', a:gui)
endfunction

function! colorconvert#rgb_to_cterm(rgb)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_rgb_to_cterm', a:rgb)
endfunction

function! colorconvert#rgb_to_gui(rgb)
	return colorconvert#invoke(g:colorconvert_instance, 'vim_rgb_to_gui', a:rgb)
endfunction

function! colorconvert#available()
	return 1
endfunction

let &cpo = s:cpo_save
unlet s:cpo_save
