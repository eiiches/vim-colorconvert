colorconvert.vim
================

This plugin offers functions for converting cterm colors to
GUI colors and vice versa. You need to have python interface compiled in vim.

Configuration
-------------

`g:colorconvert_profile`: Specify color profile for the terminal. Options are `'GnomeTerminal.Linux'`(default), `'GnomeTerminal.Tango'` and `'XTerm'`.

Example:

	let g:colorconvert_profile = 'GnomeTerminal.Tango'

Functions
---------

`colorconvert#cterm_to_gui(cterm)`

`colorconvert#gui_to_cterm(gui)`

`colorconvert#cterm_to_rgb(cterm)`

`colorconvert#gui_to_rgb(gui)`

`colorconvert#rgb_to_cterm(rgb)`

`colorconvert#rgb_to_gui(rgb)`

Examples
--------

	echo colorconvert#gui_to_cterm("#FF0")          #=>   226               
	echo colorconvert#gui_to_cterm("FF0")           #=>   226               
	echo colorconvert#gui_to_cterm("#FF0000")       #=>   196               
	echo colorconvert#gui_to_cterm("red")           #=>   red               
	echo colorconvert#cterm_to_gui(0)               #=>   #000000           
	echo colorconvert#cterm_to_gui(3)               #=>   #AA5500           
	echo colorconvert#cterm_to_gui(226)             #=>   #FFFF00           
	echo colorconvert#cterm_to_gui("226")           #=>   #FFFF00           
	echo colorconvert#cterm_to_rgb(0)               #=>   [0, 0, 0]         
	echo colorconvert#cterm_to_rgb(3)               #=>   [170, 85, 0]      
	echo colorconvert#cterm_to_rgb(226)             #=>   [255, 255, 0]     
	echo colorconvert#cterm_to_rgb("226")           #=>   [255, 255, 0]     
	echo colorconvert#cterm_to_rgb('Red')           #=>   [255, 85, 85]     
	echo colorconvert#gui_to_rgb("#FF0")            #=>   [255, 255, 0]     
	echo colorconvert#gui_to_rgb("FF0")             #=>   [255, 255, 0]     
	echo colorconvert#gui_to_rgb("#FF0000")         #=>   [255, 0, 0]       
	echo colorconvert#gui_to_rgb("red")             #=>   [255, 85, 85]     
	echo colorconvert#rgb_to_cterm([255, 0, 0])     #=>   196               
	echo colorconvert#rgb_to_gui([255, 0, 0])       #=>   #FF0000           
