from sympy import *

def infinite_sum():
    n=symbols('n', integer=True)
    expr = (1/4)*(-3/4)**(n-1)
    result = summation(expr, (n, 1, oo))
    print(result)


def prime_factorization(n):
    """
    Returns the prime factors of your number, and their integer exponents
    """
    import sympy
    factors = sympy.primefactors(n)
    for prime in factors:
        exponent = 1
        while prime % (prime**exponent) == 0:
            exponent = exponent + 1
        exponent = exponent - 1
        print(prime, exponent)
