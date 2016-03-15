class MemoryManager:
    def __init__(self):
        self.addrs = {'IN':0,'IN1':1,'OUT':2,'OUT1':3}
        self.frame_sizes = []
    def init_stack(self):
        print('#initializing stack...')
        print('set 6 1.0')
        print('set 7 50.0') # TODO: ensure beyond program
        add_frame()
    def store_register_state(self):
        print('#storing state...')
        for r in '012':
           print('store 7 '+r)
           print('add 6 7')
    def load_register_state():
        print('#loading state...')
        print('copy 0 3')
        for r in '210':
           print('sub 6 7')
           print('load 7 '+r)
    def add_frame(self, varname):
        self.frame_sizes.append(0)
    def ensure_alloc(self, varname):
       if varname not in self.addrs.keys(): return
       self.addrs[varname] = sum(self.frame_sizes) #slow but i'm lazy
       frame_sizes[-1] += 1
    def addr_of(self, varname):
        return self.addrs[varname]
    def pop_frame():
        self.frame_sizes.pop()
class Parser:
   def __init__(self, text):
      self.toks = text.split()
      self.pos = 0
      self.MM = MemoryManager(64, 32)
   def peek(self):
      return None if \
      self.pos>=len(self.toks) \
      else self.toks[self.pos]
   def rec(self, tok):
      assert(self.peek()==tok)
      self.pos += 1
   def rec_atom(self):
      if self.peek() == '(':
         self.M.store_state()
         self.rec('(')
         self.rec_expr()
         self.rec(')')
         self.M.load_state()
      elif self.peek().isalpha():
          varname = self.peek()
          print('set 4 %f' % self.MM.addr_of(varname))
          print('load 4 0')
          self.rec(varname)
      else:
         num = self.peek()
         print('set 0 '+num)
         self.rec(num)
   def rec_term(self):
      self.rec_atom()
      while self.peek() == '*':
         self.rec('*')
         print('copy 0 1')
         self.rec_atom()
         print('mul 1 0')
   def rec_expr(self):
      self.rec_term()
      while self.peek() == '+':
         self.rec('+')
         print('copy 0 2')
         self.rec_term()
         print('add 2 0')
   def rec_assign(self):
      varname = self.peek() #TODO: ensure valid
      self.MM.ensure_alloc(varname)
      self.rec(varname)
      self.rec('=')
      self.rec_expr();
      self.rec(';')
      print('set 4 %f' % self.MM.addrs[varname])
      print('store 4 0')
   def rec_statement(self):
       if self.peek() == '{':
           self.rec('{')
           self.M.add_frame()
           self.rec_block()
           self.M.pop_frame()
           self.rec('}')
       else:
           self.rec_assign()
   def rec_block(self):
       self.rec_statement()
       while self.peek():
          self.rec_statement()
   def rec_program(self):
      self.rec_block()
   def parse(self):
       self.M.init_stack()
       self.rec_program()
       print('set 4 -1.0')
       print('jump 4 0')

code = '''
x = 1.0 + 6.0 ;
y = IN ;
OUT = x + y ;
'''
P = Parser(code)
P.parse()
