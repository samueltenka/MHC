'''
0. Introduction
   Here's a small code sample that parses math formulas such as
      (x+y*45/(9-4))+4+5+6 < 4  &&  (1-9 == 45)
   Errors will trigger an abort, along with message `Ouch!`.
   To use: run on command line and enter in an expression.

1. Formal Grammar for C--
   This document is an initial step toward a parser for the
   C-- minilanguage. The syntax we separate into two parts,
   only the initial part of which we treat here:
   FORMULA MINILANGUAGE:
      [atom] <-- [(sum)] OR [number] OR [identifier]
      [product] <-- [atom] [atom*product] OR [atom/product]
      [sum] <-- [product] OR [product+sum] OR [product-sum]

      [comparison] <-- [sum] OR [sum<sum] OR [sum==sum] OR [sum>sum]
      [latom] <-- [comparison]
      [lproduct] <-- [latom] OR [latom && sum]
      [lsum] <-- [lproduct] OR [lproduct || lsum]

      [expression] <-- [lsum]
   STATEMENTS:
      [statement] <-- [{multi}] OR [if conditional] OR [while repetitive] OR [assignment]
      [assignment] <-- [identifier=term;]
      [conditional] <-- [(expression) statement]
      [repetitive] <-- [(expression) statement]
      [multi] <-- [statement] OR [statement;multi]

   Note: latom has no option for [(lsum)],
         and the grammar contains seemingly substitutions (conditional/repetitive).
         You can ask Sam about this during Q&A.
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
      #print(self.words)
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
   def finish(self):
       if not self.is_at_end():
           raise ParsingException('I finished parsing partway through. '+\
           "Did you forget to write a connecting symbol bewtween '%s' and '%s'?"%\
           (''.join(self.words[:self.pos]), ''.join(self.words[self.pos:])), self.pos)

class Generator:
   def __init__(self):
      self.out=''
   def output(self, message):
      self.out += message

class FormulaParser(Lexer, Generator):
   '''Derived directly from formal grammars.'''
   def __init__(self, text):
        Lexer.__init__(self,text, symbols='( ) * / + - < == > && || { }'.split(' '))
        Generator.__init__(self)
   def eat_number_or_variable(self):
       self.eat(self.peek(),literal=True)
   def eat_atom(self):
      if self.peek()=='(':
          self.eat('(')
          self.eat_lsum()
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
      if self.peek()=='<':
          self.eat('<')
          self.eat_sum()
      elif self.peek()=='==':
          self.eat('==')
          self.eat_sum()
      elif self.peek()=='>':
          self.eat('>')
          self.eat_sum()
   def eat_latom(self):
      #no parenthesis option
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
      self.finish()
      print('expression is OK!')

import sys
while True:
   P = FormulaParser(input())
   try:
      P.eat_expression() ## Parsing happens here.
   except ParsingException as e:
       print('''Ouch! Error around position %d: \n   %s''' % (e.position, e.message))
   print()
