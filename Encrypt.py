import string
import random

import primes
class Caesar:
    """Holds settings for parameters of Caesar Cipher.

    Processes input to encrypt/decrypt with these settings.

    Attributes:
        charRange(tuple of 2 ints): Integer tuple which describes the
            ascii start and end of valid characters for input/output.
        exceptOutOfRange(bool): If true, will raise value error when
            processing input character out of range. Else will just return the
            char.
        key(int): Caesar cipher key

    """
    def __init__(self, charRange, key, exceptOutOfRange):
        """Creates Caesar object which will encrypt/decrypt Caesar cipher

        Args:
            charRange(tuple of 2 ints): Integer tuple which describes the
            ascii start and end of valid characters for input/output.
            exceptOutOfRange(bool): If true, will raise value error when
            processing input character out of range. Else will just return the
            char.
            key(int): Caesar cipher key

        """
            
        self.charRange = charRange
        self.key = key
        self.exceptOutOfRange = exceptOutOfRange
    def encrypt (self, inputStr, decrypt=False):
        """Processes a string with the Caesar cipher settings.

        If self.exceptOutOfRange is false, out of range characters will be
        left as they are. If it true, a ValueError will be raised at any
        out of range characters.

        Args:
            inputStr(str): String to be encrypted with Caesar Cipher
            decyrpt(bool): If true, it will reverse the encryption. Default is false
        Returns:
            String that is inputStr encrypted with Caesar cipher.

        Raises:
            ValueError: If self.exceptOutOfRange is true and an invalid character is encountered.

        """
        output = ""
        keyVal = self.key if not decrypt else self.key*-1 
        for c in inputStr:
            if self.isInRange(c):
                intVal = ord(c)
                normalizedNew = (intVal - self.charRange[0] + keyVal) %(self.charRange[1]-self.charRange[0]+1) #since we're %ing over an exclusive range we have to add 1 so 0 will happen
                output+= chr(normalizedNew +self.charRange[0])
            else:
                if self.exceptOutOfRange:
                    raise ValueError(c + " is out of range: " +str(self.charRange))
                else:
                    output += c
        return output
    def isInRange(self,c):
        """Returns whether c is in the inclusive charRange

        Args:
            c(str): A string of length 1 OR an integer representing a chracter
        Returns:
             True if in range, False if out of range.

        """
         
        intVal = ord(c)
        return intVal >= self.charRange[0] and intVal<= self.charRange[1]
    def decrypt(self, inputStr):
        """Convenience method that does the same thing as encrypt(inputStr,true"""
        return self.encrypt(inputStr,True)

class Vigenere:
    """Holds settings for parameters of Vigenere Cipher.

    Processes input to encrypt/decrypt with these settings.

    Attributes:
        charRange(tuple of 2 ints): Integer tuple which describes the
            ascii start and end of valid characters for input/output.
        exceptOutOfRange(bool): If true, will raise value error when
            processing input character out of range. Else will just return the
            char.
        key(string): Vigenere cipher key

    """

    def __init__(self, charRange, key, exceptOutOfRange):
        """Creates Caesar object which will encrypt/decrypt Caesar cipher

        Args:
            charRange(tuple of 2 ints): Integer tuple which describes the
            ascii start and end of valid characters for input/output.
            exceptOutOfRange(bool): If true, will raise value error when
            processing input character out of range. Else will just return the
            char.
            key(int): Vigenere cipher key

        """

        self.charRange = charRange
        self.key = key
        self.exceptOutOfRange = exceptOutOfRange
        self.caesarProcessors = []
        for idx,c in enumerate(key):
            self.caesarProcessors.append(Caesar(charRange, ord(key[idx]), exceptOutOfRange))

    def encrypt(self, inputStr, decrypt=False):
        """Processes a string with the Vigenere cipher settings.

        If self.exceptOutOfRange is false, out of range characters will be
        left as they are. If it true, a ValueError will be raised at any
        out of range characters.

        Args:
            inputStr(str): String to be encrypted with Vigenere Cipher
            decyrpt(bool): If true, it will reverse the encryption. Default is false
        Returns:
            String that is inputStr encrypted with Vigenere cipher.

        Raises:
            ValueError: If self.exceptOutOfRange is true and an invalid character is encountered.

        """

        output = ""
        for idx,c in enumerate(inputStr):
            output += self.caesarProcessors[idx%len(self.caesarProcessors)].encrypt(c,decrypt)
        return output
    def decrypt(self, inputStr):
        """Convenience method that does the same thing as encrypt(inputStr,true"""
        return self.encrypt(inputStr,True)
##test = Caesar((33,78),1,False)
##
####print(test.isInRange("A"))
####print(test.isInRange(" "))
####print(test.encrypt("Good morNING"))
####print(test.decrypt("!"))
####print(test.encrypt("NO"))
##
##vTest = Vigenere((33,90), "AAAAAA",False)
####print(vTest.encrypt("Good morNING"))
####print(vTest.encrypt("!",True))
##origStr = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
##print ("ORIGINAL" + origStr)
##encryptStr = vTest.encrypt(origStr)
##print("ENCRYPTED: " + encryptStr)
##decrypted = vTest.decrypt(encryptStr)
##print("DECRYPTED: " +decrypted)
##print("Test passed" if decrypted==origStr else "TEST FAILED")

def isPrimitiveRoot(g, n):
    modResults = set()
    for i in range(1,n):
        modResults.add((g**i)%n)
        if len(modResults) == n-1:
            return True
    return False

##print(isPrimitiveRoot(5,23))
##print(isPrimitiveRoot(2,4))
##print(isPrimitiveRoot(3,11))


class Locksmith: 
    """
    Generates keys for Diffie-Hellman. Vulnerable to man-in-the-middle attacks.

    Generates keys based on g and n. Can generate secret value or work with
    passed in value.
    In order to discourage key re-use (because the same session key will
    result each time) the intermediate values and keys can only be calculated
    once. You should create a new secret for each communication.

    Attributes:
      g (int) A primitive root of n
      n (int) A prime number
      randNum (int) The secret

    """
    def __init__(self,g,n,randNum=None):
        """
        Initializes the Locksmith. Can take a randNum secret key as a parameter
        or generate one.

        Args:
            g(int): A primitive root of n 
            n(int): A prime number
            randNum(int): Optional(will be generated otherwise), the secret 
          
        """
        if randNum == None:
            raise NotImplemented()
            randNum = 3 #CHANGE
        self.randNum = randNum
        if not primes.isPrimitiveRoot(g, n):
            raise ValueError(str(g) + "is not a primitive root of "+str(n))
        self.g = g
        self.n = n
        self.intermValCalced = False
        self.keyCalced = False
    #CHECK THAT THIS WOULD BE A SECUIRITY PROBLEM FOR REPEAT..
    def makeIntermediateVal(self):
        """Makes the intermediate value/public key to send to other party

        To discourage session key re-use, may only be called once.

        Returns:
          The intermediate value to be given to other party
        """
        if self.intermValCalced:
            raise ValueError("Intermediate Value should only be calculated once.")
        self.intermValCalced = True 
        return (self.g**self.randNum)%self.n
    
    def makeKey(self, otherContribution):
        """Creates a session key using secret and contribution from other party.

        To discourage session key re-use, may only be called once.

        Args:
          otherContribution(int): The result of other party's 

        Returns:
          The session key.
        """
        if self.keyCalced:
            raise ValueError("Key should only be calculated once.")
        self.keyCalced = True
        return (otherContribution**self.randNum) % self.n
        
alice = Locksmith(5,23,6)
bob = Locksmith(5,23,15)
print(bob.makeKey(alice.makeIntermediateVal()))
print(alice.makeKey(bob.makeIntermediateVal()))
