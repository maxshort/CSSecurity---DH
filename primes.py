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

#not sure if this belongs...
def randomSecret():
    """returns a number between 0 and 128, inclusive"""
    return ord(os.urandom(1))//2

