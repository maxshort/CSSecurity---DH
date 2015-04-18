import os

"""Functions that have to do with prime number operations"""

def genPrime(knownPrimes):
    """Takes a list of all sorted known primes and returns the next one"""

    if len(knownPrimes) == 0: return 2
    lastKnownPrime = knownPrimes[-1]
    if lastKnownPrime == 2: return 3
    testCase = lastKnownPrime+2
    while True:
        foundOne = False
        for p in knownPrimes:
            if testCase%p == 0:
                foundOne = True
                break
        if not foundOne:
            return testCase #Made it through, not divisible by anything
        testCase += 2

def findPrime(primeNum):
    """Finds the primeNumth prime"""
    primes = []
    while len(primes) < primeNum:
        primes.append(genPrime(primes))
    return primes[-1]

def isPrimitiveRoot(g, n):
    """Checks that g is a primitive root of n"""
    modResults = set()
    for i in range(1,n):
        modResults.add((g**i)%n)
        if len(modResults) == n-1:
            return True
    return False

def diffeGen():
    """Returns a valid Diffe-Hellman g and n where g is a primiive root of n

    g will be 2 80% of the time and 7 20% of the time.

    n will be between the 20th and 35th prime number.

    Returns:
      A tuple consisting of (g, n)
    
    """

    gDecide = os.urandom(1))
    nDecide = os.urandom(1))
    if (gDecide < 205):
        g = 2
    else:
        g = 7

    

diffeGen()
