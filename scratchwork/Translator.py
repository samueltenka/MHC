'''
0. Introduction
   Here's a small code sample that translates between two
   formal grammars for algebraic expressions, namely:
   `Reverse Polish Notation` (RPN), and the ordinary way (OW)
   For example,
               OW                      RPN
           '1+2+3+4'               '4 3 2 1 + + +'
           'x+2*(y+3) + 4'         '4 3 y + 2 * x + +'
   Errors will trigger an abort, along with message `Ouch!`.

1. Formal Grammars
   For reference, the formal grammars are:
   OW:
      expression <-- term OR term + expression
      term <-- factor OR factor * term
      factor <-- (expression) OR number OR letter
   RPN:
      expression <-- term OR expression term +
      term <-- factor OR term factor *
      factor <-- expression OR number OR letter

2. Design
   We'll write two translators. They'll share many similarities:
   for example, both will handle errors, standardize whitespace,
   and keep track of their position in their input text. Thus,
   we want to wrap that shared portion in a separate function or
   class. Since we'll need to store _state_, a class is more appropriate.

   Thus, let's try 4 classes:
      a. A little exception-handling class `ParsingException`
      b. The `Lexer` class
      c. The `OW_to_RPN` class   \___ here's where the translation
      d. The `RPN_to_OW` class   /    actually happens

   The formal linguist may be interested in the similarity of
   structure between the code in (c) and (d) and our formal grammars.
'''

class ParsingException(Exception):
    def __init__(self, message, position):
        self.message, self.position = message, position

class Lexer:
   ''' Initialized with some text, which it analyzes into words.
   For example, '42*(y+z)' has 7 words. Provides interface for the
   access and translation of these words.
   '''
   def __init__(self, text):
      for punct in '()*+':
         text = text.replace(punct, ' %s '%punct)
      self.words = [word for word in text.split() if word]
      self.pos = 0
      self.out = ''
   def is_at_end(self):
      return self.pos>=len(self.words)
   def peek(self):
      if self.is_at_end():
          return None
          raise ParsingException("I don't understand sentence fragments", self.pos)
      return self.words[self.pos]
   def eat(self, tok, literal=False):
      if self.peek() != tok:
          raise ParsingException('I expected `%s` but see `%s`' % (tok, self.peek()), self.pos)
      if literal and not self.peek().replace('.','').isalnum():
          raise ParsingException('I expected a number or letter but see `%s`' % self.peek(), self.pos)
      self.pos += 1
   def output(self, message):
      self.out += message

class OW_to_RPN(Lexer):
   '''Derived directly from formal grammars.'''
   def __init__(self, text):
        Lexer.__init__(self,text)
   def eat_expr(self):
      self.eat_term()
      if self.peek() == '+':
         self.eat('+')
         self.eat_expr()
         self.output(' +')
   def eat_term(self):
      self.eat_factor()
      if self.peek() == '*':
         self.eat('*')
         self.eat_term()
         self.output(' *')
   def eat_factor(self):
      if self.peek() == '(':
         self.eat('(')
         self.eat_expr()
         self.eat(')')
      else:
         factor = self.peek()
         self.output(' %s'%factor)
         self.eat(factor,literal=True)

class RPN_to_OW(Lexer):
   '''Derived from formal grammars. Note that, internally,
   `self.words` is reversed, for easier parsing. (That way,
   we see whether the operation is `+` or `*` near the start
   of the string.)'''
   def __init__(self, text):
        Lexer.__init__(self,text)
        self.words.reverse() ## so now we're in forward polish notation
   def eat_expr(self):
      if self.peek() != '+': self.eat_term()
      else:
          self.eat('+')
          self.eat_expr()
          self.output('+')
          self.eat_term()
   def eat_term(self):
      if self.peek() != '*': self.eat_factor()
      else:
          self.eat('*')
          self.eat_term()
          self.output('*')
          self.eat_factor()
   def eat_factor(self):
      if self.peek() in '*+': ## An expression will start with * or +
         self.output('(')
         self.eat_expr()
         self.output(')')
      else:
         factor = self.peek()
         self.output('%s'%factor)
         self.eat(factor,literal=True)

'''
3. Entry Point Explanation
We come now to the entry point to code's execution:
Note how we exit if this module is not being run as
`__main__`; this allows the code above to be integrated
into a future project without the code below needing
to be run. Observe also how we parse command line
arguments and from those select an action. And finally,
note our basic exception-handling. (Because `RPN_to_OW`'s
words are reversed, `e.position` is backward. Oh well.)
'''

import sys
if __name__ != '__main__':
    sys.exit()

flag, source = sys.argv[1], ' '.join(sys.argv[2:])
P = (OW_to_RPN if flag=='-torpn' else RPN_to_OW)(source)
try:
   P.eat_expr() ## Translation happens here.
   print(P.out)
except ParsingException as e:
    print('''Ouch! Error around position %d:
    %s''' % (e.position, e.message))
