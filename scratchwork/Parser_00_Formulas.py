'''
0. Introduction
   Here's a small code sample that parses programs written
   in a minilanguage, C--, into an assembly language we'll
   call LC3K.
   Errors will trigger an abort, along with message `Ouch!`.

1. Formal Grammar for C--
   We describe the syntax in 4 parts:
   FORMULA MINILANGUAGE:
      [expression] <-- [term] OR [term+expression] OR [term-expression]
      [term] <-- [factor] OR [factor*term] OR [factor/term]
      [factor] <-- [(expression)] OR [number] OR [identifier] OR [arrayfactor] OR [procedurefactor]
   ARRAYS:
      [arrayfactor] = [factor[expression]]
   STATEMENTS:
      [statement] <-- [assignment] OR [if gaurded] OR [while gaurded] OR [{multi}]
      [assignment] <-- [identifier=term;]
      [gaurded] <-- [(expression) statement]
      [multi] <-- [statement] OR [statement;multi]
   PROCEDURES:
      [inputs] <-- [identifier] OR [identifier,inputs]
      [procedure] <-- [identifier(inputs) statement]
      [procedurefactor] <-- [identifier(inputs)]

2. LC3K
'''


class ParsingException(Exception):
    def __init__(self, message, position):
        self.message, self.position = message, position

class Lexer:
   ''' Initialized with some text, which it analyzes into words.
   For example, '42*(y+z)' has 7 words: '42', '*', '(', 'y', '+', 'z', ')'.
   Provides interface for the access and translation of those words.
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
          raise ParsingException("I don't understand sentence fragments", self.pos)
      return self.words[self.pos]
   def eat(self, tok, literal=False):
      if self.peek() != tok:
          raise ParsingException('I expected `%s` but see `%s`' % (tok, self.peek()), self.pos)
      if literal and not self.peek().replace('.','').isalnum():
          raise ParsingException('I expected a number or variable name but see `%s`' % self.peek(), self.pos)
      self.pos += 1
   def output(self, message):
      self.out += message
