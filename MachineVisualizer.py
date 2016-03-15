import tkinter as tk
import MCEditor
import Machine
import PrettyPrint as PP
import sys

class MachineGUI:
    UPDATE_DELAY = 50 #ms
    def __init__(self, master, M):
        self.M = M

        self.controls_frame = tk.Frame(master, relief=tk.SUNKEN, background='black')
        self.lblRegs = tk.Label(self.controls_frame, text="regs:", background='black',foreground='white',font = ("Courier",8))
        self.lblMemory = tk.Label(self.controls_frame, text="Memory:", background='black',foreground='white',
           font = ("Courier",8))
        self.lblCounts = tk.Label(self.controls_frame, text="[][]", background='black',foreground='white',
           font = ("Courier",8))
        self.ents = [tk.Entry(self.controls_frame, background='grey',foreground='white') for i in range(1)]
        self.lblOut = tk.Label(self.controls_frame, text="[][]", background='black',foreground='white',
                  font = ("Courier",8))

        self.on = False
        self.instr_count = 0
        self.btnRun = tk.Button(self.controls_frame, text="Run", background='black',foreground='white', command=self.turnon)
        self.btnStop = tk.Button(self.controls_frame, text="Stop", background='black',foreground='white', command=self.turnoff)

        self.lblRegs.pack()
        self.lblMemory.pack()
        self.lblCounts.pack()
        self.btnRun.pack(side=tk.LEFT)
        for e in self.ents: e.pack()
        self.lblOut.pack()
        self.btnStop.pack(side=tk.RIGHT)
        self.controls_frame.pack()

        self.pane = tk.PanedWindow(master, orient=tk.HORIZONTAL, opaqueresize=True)
        self.ed = MCEditor.EditorClass(window)

        self.pane.add(self.ed.frame)
        self.pane.pack(fill='both', expand=1)


    def turnon(self):
        self.instr_count = 0
        self.M.program_counter=2
        lines = self.ed.text.get('0.0',tk.END).split('\n')
        lines = [l.split('#')[0].strip() for l in lines]
        lines = [l for l in lines if l]
        inputs = [e.get() for e in self.ents]
        M.load_program(lines, [0] if inputs==[''] else [eval(i) for i in inputs])

        self.on=True
        self.step()
    def turnoff(self):
        self.on=False
    def step(self):
        if self.on:
           self.M.step()
           self.instr_count += 1
           self.render()
           if M.halted:
               self.turnoff()
           else:
              self.pane.after(self.__class__.UPDATE_DELAY, self.step)
    def render(self, octas_of_memory=8):
        self.lblRegs['text'] = "regs:\t" + ''.join(PP.pretty_print(r, minlen=9) for r in M.regs)
        self.lblMemory['text'] = "Memory:\n" + \
           '\n'.join(''.join(PP.pretty_print(a, minlen=10) for a in M.memory[8*i:8*i+8]) for i in range(octas_of_memory))
        self.lblCounts['text'] = '[%d instructions so far] [about to execute address %s]' % (self.instr_count,self.M.program_counter)
        self.lblOut['text'] = str(self.M.memory[1:2])

window = tk.Tk()
window.title("Machine")
window.geometry("640x480")
window.wm_iconbitmap("MH.ico")
window.configure(background='black')

M = Machine.Machine(num_regs=8, num_addresses=64)
MGUI = MachineGUI(window, M)
MGUI.render()

window.mainloop()
