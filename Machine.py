#Michigan Hackers Presentation on Compilers
import EnsureVersion3

'''
instructions:
add     A   B   D   R[D] <-- R[A] + R[B]
sub     A   B   D   R[D] <-- R[A] - R[B]
mul     A   B   D   R[D] <-- R[A] * R[B]
div     A   B   D   R[D] <-- R[A] // R[B]
load    A   D   m   R[D] <-- M[m+R[A]]
store   A   D   m   R[D] --> M[m+R[A]]
biz     A   m         PC <-- m-1 if A==0 else PC
halt                terminate execution.

Note: program might also contain literal numbers in addition to instructions.

Machine Specifics:
Each memory address contains an integer or program instruction.
The program counter starts at 2.
The first 2 memory addresses represent IO devices:
0           [Input, e.g. joystick angle]
1           [Output, e.g. pixel value]
2,3,...     [Program then data]
'''

class Machine:
   def __init__(self, num_addresses, num_regs):
      self.memory = [0 for i in range(num_addresses)]
      self.regs = [0 for i in range(num_regs)]
      self.program_counter = None
      self.halted = False
   def load_program(self, lines, inputs=(0,)):
       self.memory[:1]=inputs
       self.program_counter = 2
       for i in range(len(lines)):
           words = lines[i].split(' '); assert(words)
           if not words[0].isalpha(): lines[i]=eval(lines[i])
           self.memory[self.program_counter+i] = lines[i]
       self.halted = False
   def print_mem(self, l=8):
      print('memory', ' '.join(str(s).replace(' ','_') for s in self.memory[:l])+'. . .')
      print('regs', self.regs)
   def step(self):
      assert(not self.halted)
      instr = self.memory[self.program_counter]
      print('instr #%d: [%s]' % (self.program_counter, instr))
      words = instr.split(' ')
      command, args = words[0], words[1:]
      getattr(self,command)(*[eval(a) for a in args if a])
      self.program_counter += 1

   def add(self, a, b, d): self.regs[d] = self.regs[a] + self.regs[b]
   def sub(self, a, b, d): self.regs[d] = self.regs[a] - self.regs[b]
   def mul(self, a, b, d): self.regs[d] = self.regs[a] * self.regs[b]
   def div(self, a, b, d): self.regs[d] = self.regs[a] // self.regs[b]

   def load(self, A, D, m): self.regs[D] = self.memory[m+self.regs[A]]
   def store(self, A, D, m): self.memory[m+self.regs[A]] = self.regs[D]
   def biz(self, a, m): #branch if 0
       if self.regs[a]==0:
           self.program_counter = m-1
   def halt(self): #branch if 0
       self.halted = True
