# coding: utf-8
# Módulo números de Fibonacci

def fib(n):
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
        return a
        print (fib(n))

def fib2(n):   # devolve a série de Fibonacci de 0 até n
    resultado = []
    a = 0
    b = 1
    while b < n:
        resultado.append(b)
        a, b = b, a+b
    return resultado
