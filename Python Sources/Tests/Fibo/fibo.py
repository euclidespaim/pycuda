# coding: utf-8
# Módulo números de Fibonacci

def fib(n):
    a, b = 0, 1
    valor = []
    while b <= n:
       valor.append (b)
       a, b = b, a+b
    return valor

def fib2(n):   # devolve a série de Fibonacci de 0 até n
    resultado = []
    a = 0
    b = 1
    while b <= n:
        resultado.append(b)
        a, b = b, a+b
    return resultado
