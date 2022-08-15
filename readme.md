# AccessVPad - ReadMe

AccessVPad serves as an add-on to provide an accessible virtual two-dimensional reading/writing pad, which derives from the concept of grid, and is equipped with a variety of interactive functions via keyboard input and speech output. 

The current available text editor could only be edited in a horizontal direction, which limits the readability and the expression in mathematics, especially when expressing the two-dimensional calculating procedure in a vertical form, and hence makes communication and teaching inefficient for visually impaired people.

AccessVPad aims to solve the limitation of the current available text editors by enabling calculations where vertical alignment is required. For instance, in occasions of calculating unit conversion or polynomials, AccessVPad allows users to learn and express the arithmetic concept of carry or any occasions where vertical alignment could help deliver in a more intuitive and efficient way.

## Features

Press NVDA+Alt+D to activate the AccessVPad control panel.

When there is no open pad, press the pad button to add a new pad. After choosing the type of the new pad, press enter to finish creating a virtual writing pad. The pad could be input via keyboard and output through speech.

There are currently 2 types of pads available, Plane and Table, which are both grid-based structures. The difference is whether it could be input with multiple characters in one cell. Plane only allows one character in each cell; whereas Table could deal with multiple characters in a cell. Hence, Plane is ideal for situations when visual alignment is based on characters, e.g. vertical addition or vertical multiplication, while Table is suitable for situations where visual alignment should be based on blocks, e.g. polynomial or determinant calculation.

## General Commands

### To Switch between pads: in reference to general keyboard shortcuts.

*	Ctrl + Page Up / Ctrl + Shift + tab : Switch backward one pad to the previous pad. When there is no previous pad, switch backward to the latest pad.
*	Ctrl + Page Down / Ctrl + tab : Switch forward one pad to the next pad, when there is no next pad, switch forward to the very first pad.
*	Ctrl + Num key (1~9) : Switch to the pad according to ordinal number.

### Move: Read out the content when moving to a new cell.

*	Up Arrow: Move the cursor one distance up. (column number stays the same; row number -1)
*	Down Arrow: Move the cursor one distance down. (column number stays the same; row number +1)
*	Left Arrow: Move the cursor one distance left. (column number -1; row number stays the same)
*	Right Arrow: Move the cursor one distance right (column number +1; row number stays the same)
*	Home: Move the cursor to the leftmost cell in the same row.
*	End: Move the cursor to the rightmost cell in the same row.
*	Shift + Home: Move the cursor to the very top cell in the same column.
*	Shift + End: Move the cursor to the bottom cell in the same column.

### Update: To modify the content in a cell; to add/delete a column/row; to add/delete a pad

*	Character (EN or Num) keys: To input content from where the cursor locates.
*	Alt + Up Arrow: To insert a new row above the cursor.
*	Alt + Down Arrow: To insert a new row below the cursor.
*	Alt + Left Arrow: To insert a new column at the left side of the cursor.
*	Alt + Right Arrow: To insert a new column at the right side of the cursor.
*	Alt + Delete: To delete the row of the current cursor.
*	Alt + Shift + Delete: To delete the column of the current cursor.
*	Ctrl + n: To add a new pad.
*	Ctrl + o: To open a csv file on the computer.
*	Ctrl + s: To save and export the file in csv format.
*	Ctrl + w: To close the current pad.

### Read

*	Num key (1~9): Read out the content same as NVDA Reviewing text function
*	NVDA+numpadDelete: Read out the column/row number of the current cell. Double *fast click* to read out the total column/row number of the total range.

### GUI (Graphical User Interface) Menu

GUI of AccessVPad locates at Tools -> AccessVPad menu.

Pad: Press NVDA+Alt+D to activate the AccessVPad control panel.

Browser: Open browser to sync view the active pad in AccessVPad.

 Settings：

*	Adjust the style of page on browser:
	*	Show the border of the total range.
	*	Show where the cursor locates with the chosen highlighted colour. 
