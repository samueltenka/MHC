'''
Thanks to Robert@pytrash (see link below)
http://tk.unpythonic.net/wiki/A_Text_Widget_with_Line_Numbers
'''

import tkinter as tk

class EditorClass(object):
    UPDATE_PERIOD = 30 #ms
    updateId = None
    def __init__(self, master):
        self.lineNumbers = ''
        # A frame to hold the three components of the widget.
        self.frame = tk.Frame(master, relief=tk.SUNKEN)
        # The widgets vertical scrollbar
        self.vScrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.vScrollbar.pack(fill='y', side=tk.RIGHT)
        # The Text widget holding the line numbers.
        self.lnText = tk.Text(self.frame,
                width = 4,
                padx = 4,
                background = 'black',
                foreground = 'grey',
                state='disabled'
        )
        self.lnText.pack(side=tk.LEFT, fill='y')
        # The Main Text Widget
        self.text = tk.Text(self.frame,
                undo=True,
                foreground='white',
                insertbackground='green',
                background = 'black'
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.text.config(yscrollcommand=self.vScrollbar.set)
        self.vScrollbar.config(command=self.text.yview)
        if self.__class__.updateId is None:
            self.updateAllLineNumbers()

    def getLineNumbers(self):
        offset = 2-1 #start numbering at line 2
        line = '%d' % offset
        col= ''
        ln = ''
        # assume each line is at least 6 pixels high
        step = 6
        nl = '\n'
        lineMask = '    %s\n'
        indexMask = '@0,%d'
        for i in range(0, self.text.winfo_height(), step):
            ll, cc = self.text.index( indexMask % i).split('.')
            ll2 = str(offset+int(ll))
            if line == ll:
                if col != cc:
                    col = cc
                    ln += nl
            elif self.text.get('%s.0' % ll) == '#':
               line,col=ll,cc
               ln += nl
               offset -= 1
            else:
                line, col = ll, cc
                ln += (lineMask % ll2)[-5:]
        return ln
    def updateLineNumbers(self):
        tt = self.lnText
        ln = self.getLineNumbers()
        if self.lineNumbers != ln:
            self.lineNumbers = ln
            tt.config(state='normal')
            tt.delete('1.0', tk.END)
            tt.insert('1.0', self.lineNumbers)
            tt.config(state='disabled')
    def updateAllLineNumbers(self):
        self.updateLineNumbers()
        self.__class__.updateId = self.text.after(
            self.__class__.UPDATE_PERIOD,
            self.updateAllLineNumbers)
