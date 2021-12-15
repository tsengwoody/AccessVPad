# AccessVPad - ReadMe

This addon provides a virtual 2 dimensional reading/writing pad, which derives from the concept of grid, and equipped with a variety of interactive functions via keyboard input and speech output. The current available text editor could only be edited in a letter-based, horizontal direction, which limits the readability and the expression in mathematics, especially the (2 dimensional) calculating procedure in vertical form, and hence makes communication and teaching inefficient for visually impaired people.

This addon aims to solve the limitation of the current available text editors by enabling calculations where (visual) vertical alignment is required (to be aligned vertically). For instance, in occasions of calculating unit conversion or polynomials, the 2 dimensional vertical calculator allows users to learn and express the arithmetic concept of carry or any occasions where vertical alignment could help to be delivered in a more intuitive and efficient way.

## Feature

Press NVDA+Alt+D to activate the AccessVPad control panel.

When there is no open tab in the panel, press the pad button to add a new tab, after choosing the type of the new panel, press enter to create a virtual writing tab. The virtual writing tab could be input via keyboard and output through speech.

There are currently 2 types of panels available, Plane and Table, both are grid-based structures. The difference is whether it could be input with multiple letters in one cell. Plane could only allow one letter in each cell, whereas Table could deal with multiple letters in a cell. Hence, Plane is ideal for situations when visual alignment is based on letters, e.g. vertical addition or vertical multiplication, while Table is suitable for situations where visual alignment should be based on blocks, e.g. polynomial or determinant calculation.

### For Switching between window tabs: in reference to general keyboard shortcuts for multiple window application.

*	Ctrl + Up Arrow / Ctrl + Shift + tab : Switch backward one tab to the previous tab. When there is no previous tab, switch backward to the latest tab.
*	Ctrl + Down Arrow / Ctrl +tab: Switch forward one tab to the next tab, when there is no next tab, switch forward to the very first tab.
*	Ctrl + Num key (1~9): Switch to the tab according to ordinal number.

### Move: Read out the content when moving to a new cell.

*	Up Arrow: Move the cursor one distance up. (column -1; row number stays the same)
*	Down Arrow: Move the cursor one distance down. (column +1; row number stays the same)
*	Left Arrow: Move the cursor one distance left. (column number stays the same; row -1)
*	Right Arrow: Move the cursor one distance right (column number stays the same; row+1)
*	home: Move the cursor to the leftmost cell in the same row.* end: Move the cursor to the rightmost cell in the same row.
*	shift+home: Move the cursor to the very top cell in the same column.
*	shift+end: Move the cursor to the bottom cell in the same column.

### Update: To modify the content in a cell; to add/delete a column/row; to add/delete a tab

*	EN or Num key: To input content from when the cursor locates.
*	Alt + Up Arrow: To insert a new row above the cursor.
*	Alt + Down Arrow: To insert a new row below the cursor.
*	Alt + Left Arrow: To insert a column at the left side of the cursor.
*	Alt + Right Arrow: To insert a column at the right side of the cursor.
*	Alt + delete: To delete the row of the current cursor.
*	Alt + shift + delete: To delete the column of the current cursor.
*	Ctrl + n: To add a new tab.
*	Ctrl + o: To open a csv file on the computer.
*	Ctrl + s: To save and export the file in csv format.
*	Ctrl + w: To close the current tab.

### Read

*	Num 1~9: Read out the content by line/word/character unit .
*	NVDA + Num delete: Read out the column/row number of the current cell. Double click to read out the total column/row number of the total range.

### 圖形介面選單
AccessVPad 的圖形介面集中於工具->AccessVPad選單中
* Pad：與 NVDA+alt+d 相同打開 AccessVPad 視窗
* Browser：打開瀏覽器進行同步檢視當前面版視窗內容### Picture Platform Options

The graphical interface of AccessVPad is concentrated in the Tools->AccessVPad menu

Pad: Press NVDA+Alt+D to activate the AccessVPad control panel.

Browser: Open browser to sync view the current tab in AccessVPad.

 Settings：

*	Adjust the style of page on browser:
	*	Show border of the cell
	*	Hightlight color of the cell pointed to by cursor
