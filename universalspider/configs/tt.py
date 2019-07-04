# import sys
# sys.setrecursionlimit(1000000) 


def func1(n,k):
    if n==1 or k==1 or n==0:
        return 1
    elif n<k:
        return func1(n,n)
    elif n==k:
        return 1+func1(n,k-1)
    else:
        return func1(n,k-1)+func1(n-k,k)

def func2(m,n,k):
    a = 0
    for i in range(1,min(k,m+1)):
        a += func1(m-i,i) * func1(n,k-i)
    
    return a

if __name__ == "__main__":
    print(func2(2,2,4))