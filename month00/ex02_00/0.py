from goto import with_goto
#from itertools import compress, product, chain, combinations
import itertools

def primfacs(n):
    i = 2
    primfac = []
    
    if (n == 1 or n == 0):
         primfac.append(n)
         return primfac
    
    while i * i <= n:
        while n % i == 0:
            primfac.append(i)
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(n)
    return primfac

@with_goto
def par(up, down):
    label .a
    for i in up:
        for j in down:
            if i == j:
                up.remove(i)
                down.remove(j)
                goto .a
    return (up, down)

def par_new(par1):
    up = par1[0]
    down = par1[1]
    up_new = []
    down_new = []
    for i in up:
        buf = primfacs(i)
        for j in buf:
            up_new.append(j)
    for i in down:
        buf = primfacs(i)
        for j in buf:
            down_new.append(j)
    #print(up_new)
    #print(down_new)
    return par(up_new, down_new)

def up_rez(n):
    rez = [i for i in  range(1,n+1)]
    return rez

def down_rez(m, k):
    return up_rez(m) + up_rez(k)

def c(n, m):
    if n < m:
        return ['NULL']
    up = up_rez(n)
    down = down_rez(m, n - m)
    #print(up)
    #print(down)
    par1 = par(up, down)
    par_new1 = par_new(par1)
    return par_new1[0]
    #return up / down

def combinations(s):
    rez = []
    for i in range(1,len(s)+1):
           rez.extend(list(itertools.combinations(s,i)))
    rez = list(set(rez))
    rez.sort(key=len)
    for i in range(0, len(rez)):
        list(rez[i]).sort()
        print(rez[i])
    return set(rez)
    
def binom(N):
    rez = []
    for i in range(1, N):
        buf = c(N, i)
        for j in buf:
            rez.append(j)
    return combinations(rez)

#print(primfacs(8))
print(binom(5))

