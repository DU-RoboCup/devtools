'''
The MIT License (MIT)

copyright (c) 2017 "University of Denver"

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


Created By: Paul Heinen
'''

import os
import platform
import locale
import curses
import sqlite3
from curses import wrapper

def main(stdscr):
    # Set Language Locale
    locale.setlocale(locale.LC_ALL,'')
    code = locale.getpreferredencoding()

    # Ensure that the user isn't executing the script from Windows
    if(platform.system() == 'Windows'):
        print("Sorry, the included curses python module doesn't support Windows.\nYou should be running this in the Development Environment anyway!")
        return

    # Curses draws in the weird (y,x) format from (0,0) to (MAX_HEIGHT-1, MAX_WIDTH-1)
    MAX_HEIGHT, MAX_WIDTH = curses.LINES, curses.COLS


    def main_menu():
        stdscr.clear()
        debug()

    def init_color_schemes():
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_YELLOW)

    '''
    def print_line: Print's a bunch of '=' signs.
        @param row_num: Height from top (0 indexed) to print text
        @param color_scheme: You can specify the color scheme, default is 1
    '''
    def print_line(row_num, color_scheme=1):
        for i in range(MAX_WIDTH):
            stdscr.addstr(row_num, i, "=", curses.color_pair(color_scheme))
    '''Tests (currently broken)

    def other_drawing_tests():
        def draw_symbols(row=15,col=1):
            c = curses
            symbols = [c.ACS_BBSS, c.ACS_BLOCK,c.ACS_BOARD,c.ACS_BSBS,c.ACS_BSSB,c.ACS_BSSS,c.ACS_BTEE,c.ACS_BULLET,c.ACS_CKBOARD,c.ACS_DARROW,c.ACS_DEGREE,c.ACS_DIAMOND,c.ACS_GEQUAL,c.ACS_HLINE,c.ACS_LANTERN,c.ACS_LARROW,c.ACS_LEQUAL,c.ACS_LLCORNER,c.ACS_LRCORNER,c.ACS_LTEE,c.ACS_NEQUAL,c.ACS_PI,c.ACS_PLMINUS,c.ACS_PLUS,c.ACS_RARROW,c.ACS_RTEE,c.ACS_S1,c.ACS_S3,c.ACS_S7,c.ACS_S9,c.ACS_SBBS,c.ACS_SBSB,c.ACS_SBSS,c.ACS_SSBB,c.ACS_SSBS,c.ACS_SSSB,c.ACS_SSSS,c.ACS_STERLING,c.ACS_TTEE,c.ACS_UARROW,c.ACS_ULCORNER,c.ACS_URCORNER,c.ACS_VLINE]
            for i in range(len(symbols)-1):
                stdscr.addstr(row,col,symbols[i])
                if col+1 > MAX_WIDTH: row+=1
        draw_symbols()
    '''


    '''
    def set_text_style: Helper function to choose from predefined styles for styling text
        @param text_style: A string which represents a key value for looking up in the dictionary
        return: Chosen style to be passed to another function. If style doesn't exist color_pair(1) is returned
    '''
    def set_text_style(text_style):
        Styles = {
                    '1'             : curses.color_pair(1),
                    '2'             : curses.color_pair(2),
                    '3'             : curses.color_pair(3),
                    '4'             : curses.color_pair(4),
                    'A_BLINK'       : curses.A_BLINK,
                    'A_BOLD'        : curses.A_BOLD,
                    'A_DIM'         : curses.A_DIM,
                    'A_REVERSE'     : curses.A_STANDOUT,
                    'A_UNDERLINE'   : curses.A_UNDERLINE
                 }

        return Styles[str(text_style)] if str(text_style) in Styles else Styles['1']

    '''
    def print_centered_text: Prints approx. centered text.
        @param string: Text to be printed. MUST be < MAX_WIDTH
        @param row_num: Row where the text will be printed - 0 <= row_num <= MAX_HEIGHT
        @param offset: An offset either left (-offest) or right (+offset). Must not overflow or underflow. Default val 0
        @param text_style: Custom color pair for the text. Default is 1
    '''
    def print_centered_text(string, row_num, offset=0, text_style=1):
        string = str(string) #Just in case some jerry passes a numeric value
        halfway_screen, halfway_text = int(MAX_WIDTH/2), int(len(string)/2)
        if offset + halfway_text < halfway_screen:
            stdscr.addstr(row_num, halfway_screen - halfway_text + offset, string, set_text_style(text_style))

    '''
    def interactive_menu_builder: Generates simple interactive menus.
        @param row_num: The Row number in the curses window where the menu will start
        @param col_num: The column number in the curses window where the menu will start
        @param strings_array: An array containing strings with menu items you wish to appear. Dont add #'s
        @param response_array: An array of function pointers or lambdas which are the result of selecting menu items
        @param default_selected: The menu item you wish to have initially selected
        @parm styles_array: Allows menu items to have custom styles

    NOTE: This has quite a few edge cases that could cause it to crash. Use this method with caution until further developed.
    '''
    def interactive_menu_builder(row_num, col_num,strings_array,response_array,default_selected=0,styles_array=1):
        # Add default styles if not specified
        if not isinstance(styles_array, list):
            styles_array = [styles_array for i in range(len(strings_array))]
        if not (len(styles_array) == len(strings_array)):
            assert len(styles_array) < len(strings_array)
            [styles_array.append(1) for i in range(len(strings_array) - len(styles_array))]


        if not len(strings_array) == len(response_array):
             stdscr.clear()
             stdscr.addstr(int(MAX_HEIGHT/2), int(MAX_WIDTH/2), "ERROR! Invalid Menu!", curses.color_pair(5))
             return;

        # Helper function for redrawing selected menu items
        def update_selected(item_num, d=default_selected):
            assert item_num <= len(strings_array)
            #Clear styles from default_selected/last selected item
            stdscr.addstr(row_num + d , col_num, str(d))
            #Update Selected
            stdscr.addstr(row_num + item_num, col_num, str(item_num), curses.A_BOLD | curses.A_UNDERLINE)
            stdscr.move(row_num + item_num, col_num)
        # Draw menu
        commands_dict = {}
        i = 0
        for name, style in zip(strings_array, styles_array):
            stdscr.addstr(row_num+i, col_num,"{}. {}".format(i,name), style)
            if i == default_selected:
                update_selected(default_selected)

            commands_dict.update({str(i) : response_array[i]})
            i+=1


        stdscr.move(row_num + default_selected, col_num)
        #Do UI Interaction
        while True:
            key = stdscr.getch()
            # Need try catch because keyboard inputs apparently have a lot of edge cases
            # I don't care about dealing with
            try:
                curr_selected = default_selected
                # Execute menu item. KEY_ENTER is unreliable (due to various terminal seetings) so secondary
                # check for '\r' and '\n' values (key codes 10 and 13 respectively) is required.
                if key == curses.KEY_ENTER or key == 10 or key == 13 or key == ord('e'):
                    response_array[default_selected]()
                    break
                # Handle Key Up/Down presses w/ wrap around
                # Need To Press Enter to confirm selection
                elif key == curses.KEY_UP or key == curses.KEY_DOWN:
                    # Increment/Decrement current selected
                    curr_selected = curr_selected - 1 if key == curses.KEY_UP else curr_selected + 1
                    # Wrap around the menu if needed
                    curr_selected = len(strings_array) - 1 if curr_selected < 0 else 0 if curr_selected > len(strings_array) - 1 else curr_selected
                    #default_selected + 1 if (default_selected + 1) <= len(response_array)-1 else 0
                    stdscr.addstr(14,15, "curr_selected: {} \t default_selected: {}".format(str(curr_selected), str(curr_selected)))

                    update_selected(curr_selected, default_selected)
                    default_selected = curr_selected
                    stdscr.refresh()

                # Bind Function Pointers to Key vals
                # TODO: This needs to be better tested/may be a bug farm
                elif chr(key).isdigit():
                    if int(chr(key)) in response_array:
                        response_array[i]()
                        break
            except:
                pass


### BEGIN FUNCTIONS FOR TESTING

    def test_menu():
        options = ['hello','world','foo','bar']
        hello = lambda:  stdscr.addstr(19,1,"hello")
        world = lambda: stdscr.addstr(19,5,"world")
        foo = lambda: stdscr.addstr(19, 10, "foo")
        bar = lambda: stdscr.addstr(19, 14, "bar")
        responses = [hello,world,foo,bar]
        interactive_menu_builder(7,7,options,responses)

    def debug():
        print_line(0, 4)
        print_line(3, 4)
        print_centered_text("Hello World", 2, 1, "A_BOLD")
        test_menu()

    # Exit curses and restore the terminal to normal operations mode
    # Note: For debug purposes, the curses wrapper handles a lot of this for us. It's rather annoying w/o it.
    def exit():
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()


    # Testing...
    init_color_schemes()
    main_menu()
    stdscr.getkey()

wrapper(main)
