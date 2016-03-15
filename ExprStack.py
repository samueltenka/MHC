class ExprStack:
    def __init__(self, framecapacityreg, stackreg, workregs, labelprefix='exprstk'):
        self.workregs=workregs[:]
        self.stackreg, self.framecapacityreg = stackreg, framecapacityreg
        self.memnames = ['%s%r'%(labelprefix,r) for r in self.workregs]
        self.total_els=0
        self.curr_frame_len = 0 #will == total_els (mod numregisters)
    def frame_is_empty(self):
        return self.curr_frame_len == 0
    def frame_is_full(self):
        return self.curr_frame_len == len(self.workregs)
    def stack_is_empty(self):
        return self.total_els==0
    def store(self):
        assert(self.frame_is_full())
        for r,m in zip(self.workregs, self.memnames):
           print('sw %d %d %s'%(self.stackreg,r,m))
        print('add %d %d %d' % (self.stackreg, self.framecapacityreg, self.stackreg))
        self.curr_frame_len = 0
        assert(self.frame_is_empty())
    def load(self):
        assert(self.frame_is_empty())
        print('sub %d %d %d' % (self.stackreg, self.framecapacityreg, self.stackreg))
        for r,m in zip(self.workregs, self.memnames):
           print('lw %d %d %s'%(self.stackreg,r,m))
        self.curr_frame_len = len(self.workregs)
        assert(self.frame_is_full())
    def top(self):
        '''returns register# (e.g. 0,1,...7)'''
        assert(not self.stack_is_empty())
        return self.workregs[self.curr_frame_len-1]
    def push(self):
        self.curr_frame_len += 1; self.total_els -= 1
        if self.frame_is_full():
            self.store()
    def pop(self):
        if self.frame_is_empty():
            self.load()
        self.curr_frame_len -= 1; self.total_els -= 1

if __name__=='__main__':
    ''' Test; should output string below'''
    ES = ExprStack(0,1,[2,3,4,5])
    for i in range(10):
        ES.push()
        print('new reg:',ES.top())
    for i in range(10):
        print('destroying reg:',ES.top())
        ES.pop()
    '''
new reg: 2
new reg: 3
new reg: 4
new reg: 5
sw 1 2 exprstk2
sw 1 3 exprstk3
sw 1 4 exprstk4
sw 1 5 exprstk5
add 1 0 1
new reg: 2
new reg: 3
new reg: 4
new reg: 5
sw 1 2 exprstk2
sw 1 3 exprstk3
sw 1 4 exprstk4
sw 1 5 exprstk5
add 1 0 1
new reg: 2
new reg: 3
destroying reg: 3
destroying reg: 2
sub 1 0 1
lw 1 2 exprstk2
lw 1 3 exprstk3
lw 1 4 exprstk4
lw 1 5 exprstk5
destroying reg: 5
destroying reg: 4
destroying reg: 3
destroying reg: 2
sub 1 0 1
lw 1 2 exprstk2
lw 1 3 exprstk3
lw 1 4 exprstk4
lw 1 5 exprstk5
destroying reg: 5
destroying reg: 4
destroying reg: 3
destroying reg: 2
sub 1 0 1
lw 1 2 exprstk2
lw 1 3 exprstk3
lw 1 4 exprstk4
lw 1 5 exprstk5
    '''
