'''
0. Introduction
   Here's a small code sample that parses programs written
   in a minilanguage, C--, into an assembly language we'll
   call LC3K. Errors will trigger an abort, along with message
   `Ouch!`.

1. Formal Grammar for C--
   We describe the syntax in 4 parts:
   FORMULA MINILANGUAGE:
      [atom] <-- [(sum)] OR [number] OR [identifier]
      [product] <-- [atom] [atom*product] OR [atom/product]
      [sum] <-- [product] OR [product+sum] OR [product-sum]

      [comparison] <-- [sum] OR [sum<sum] OR [sum==sum] OR [sum>sum]
      [latom] <-- [(lsum)] OR [comparison]
      [lproduct] <-- [latom] OR [latom && sum]
      [lsum] <-- [lproduct] OR [lproduct || lsum]

      [expression] <-- [lsum]
   STATEMENTS:
      [statement] <-- [{multi}] OR [if conditional] OR [while repetitive] OR [assignment]
      [assignment] <-- [identifier=term;]
      [conditional] <-- [(expression) statement]
      [repetitive] <-- [(expression) statement]
      [multi] <-- [statement] OR [statement;multi]

2. LC3K
   The assembly language will consist of 8 instruction types:
   4 for integer arithmetic, 2 for memory, and 2 for flow control.
      0. add r0 r1 rd
      1. sub r0 r1 rd
      2. mul r0 r1 rd
      3. div r0 r1 rd
      4. load r0 r1 offset
      5. store r0 r1 offset
      6. branchif0 r0 r1 label
      7. halt
'''

class ParsingException(Exception):
    def __init__(self, message, position):
        self.message, self.position = message, position

class Lexer:
   ''' Initialized with some text, which it analyzes into words
   according to specified delimiters. Provides interface for
   the access and translation of those words.
   '''
   def __init__(self, text, symbols):
      for punct in symbols:
         text = text.replace(punct, ' %s '%punct)
      self.words = [word for word in text.split() if word]
      self.pos = 0
   def is_at_end(self):
      return self.pos>=len(self.words)
   def peek(self):
      if self.is_at_end():
          return None
          #raise ParsingException("I don't understand sentence fragments", self.pos)
      return self.words[self.pos]
   def eat(self, tok, literal=False):
      if self.peek() != tok:
          raise ParsingException('I expected `%s` but see `%s`' % (tok, self.peek()), self.pos)
      if literal and (self.peek()==None or not self.peek().isalnum()): #for decimal places, we'd need to replace '.' by ''
          raise ParsingException('I expected a number or letter but see `%s`' % self.peek(), self.pos)
      self.pos += 1

class Generator:
   def __init__(self):
      self.out=''
   def output(self, message):
      self.out += message

class FormulaParser(Lexer, Generator):
   '''Derived directly from formal grammars.'''
   def __init__(self, text):
        Lexer.__init__(self,text, symbols='( ) * / + - <= == >= && || { }'.split(' '))
        Generator.__init__(self)
   def eat_number_or_variable(self):
       self.eat(self.peek(),literal=True)
   def eat_atom(self):
      if self.peek()=='(':
          self.eat('(')
          self.eat_sum()
          self.eat(')')
      else:
          self.eat_number_or_variable()
   def eat_product(self):
      self.eat_atom()
      if self.peek()=='*':
          self.eat('*')
          self.eat_product()
      elif self.peek()=='/':
          self.eat('/')
          self.eat_product()
   def eat_sum(self):
      self.eat_product()
      if self.peek()=='+':
          self.eat('+')
          self.eat_sum()
      elif self.peek()=='-':
          self.eat('-')
          self.eat_product()
   def eat_comparison(self):
      self.eat_sum()
      if self.peek()=='<=':
          self.eat('<=')
          self.eat_sum()
      elif self.peek()=='==':
          self.eat('==')
          self.eat_sum()
      elif self.peek()=='>=':
          self.eat('>=')
          self.eat_sum()
   def eat_latom(self):
      if self.peek()=='(':
          self.eat('(')
          self.eat_lsum()
          self.eat(')')
      else:
          self.eat_comparison()
   def eat_lproduct(self):
      self.eat_latom()
      if self.peek()=='&&':
          self.eat('&&')
          self.eat_lproduct()
   def eat_lsum(self):
      self.eat_lproduct()
      if self.peek()=='||':
          self.eat('||')
          self.eat_lsum()
   def eat_expression(self):
      self.eat_lsum()
      print('expression is OK!')

import sys
while True:
   P = FormulaParser(input())
   try:
      P.eat_expression() ## Parsing happens here.
   except ParsingException as e:
       print('''Ouch! Error around position %d: \n   %s''' % (e.position, e.message))
   print()
