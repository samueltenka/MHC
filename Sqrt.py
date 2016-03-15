def sqrt(n):
    if n<=0: return 0
    s = -1
    snew = 1
    while abs(s-snew)>1:
        s = snew
        snew = (s + n//s)//2
    return snew
for i in range(1000):
    assert(i==sqrt(i**2))
print("passed: sqrts of perfect squares all match")
