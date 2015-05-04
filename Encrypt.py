import string
import random
import primes
import os

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
            key(string): Vigenere cipher key

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
    passed in value. g should be a primitive root of n
    In order to discourage key re-use (because the same session key will
    result each time) the intermediate values and keys can only be calculated
    once. You should create a new secret for each communication.

    Attributes:
      g (int) A primitive root of n
      n (int) A prime number
      randNum (int) The secret

    """
    def __init__(self,g,n,randNum):
        """
        Initializes the Locksmith. 

        Args:
            g(int): A primitive root of n 
            n(int): A prime number
            randNum(int): the secret 
          
        """
        if randNum == None:
            raise NotImplemented()
            
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

class VigLocksmith(Locksmith):
    """"Geneterates a sequence of numbers from diffe-hellman to come up with a Vigenere Cipher Key

    65 is added to keys to give letters

    """

    def __init__(self, g, n, initialValue):
        """
        Initializes the Vigenere Locksmith. 

        Args:
            g(int): A primitive root of n 
            n(int): A prime number
            randNum(int): List of secret nums. Length of randomNums must be same for both parties
          
        """
        if not primes.isPrimitiveRoot(g, n):
            raise ValueError(str(g) + "is not a primitive root of "+str(n))
        self.g =g
        self.n = n
        self.initialValue = initialValue
        self.intermValCalced = False
        self.keyCalced = False

    def makeIntermediateVal(self):
        """Makes the intermediate value/public key to send to other party

        To discourage session key re-use, may only be called once.

        Returns:
          The intermediate value to be given to other party
        """
        if self.intermValCalced:
            raise ValueError("Intermediate Value should only be calculated once.")
        self.intermValCalced = True 
        return VigLocksmith.numsToKey([(self.g**randNum)%self.n for randNum in VigLocksmith.keyToNums(self.initialValue, 64)],64)

    def makeKey(self, otherContribution):
        """Creates a session key using secret list and contribution list from other party.

        To discourage session key re-use, may only be called once.

        Args:
          otherContribution(string): The result of other party's intermediate value 

        Returns:
          The session key as a string.
        """
        def convert(i):
            """Adds 65 to integer i and returns the resulting character""" 
            return chr(65+i)
        if self.keyCalced:
            raise ValueError("Key should only be calculated once.")
        self.keyCalced = True
        asNums = [(pair[1]**pair[0]) % self.n for pair in zip(VigLocksmith.keyToNums(self.initialValue,64), VigLocksmith.keyToNums(otherContribution,64))]
        return "".join(map(convert,asNums))

    @staticmethod
    def keyToNums(string,offset):
        converter = lambda c:ord(c)-offset
        return list(map(converter, string))
    
    @staticmethod
    def numsToKey(nums, offset):
        print("RECEIVED " + str(nums))
        converter = lambda i: chr(i + offset)
        return "".join(list(map(converter,nums)))

def genVigKey(length):
    """Generates a random key of upper and lowercase letters of the specified length"""
    #os.urnandom is generated by OS and supposed to be more random
    #4.48 comes from 255/57 rounded up slightly for safety
    #65 is where A starts, there is a bit of punctuation in betwen
    #122 is z 122 - 65 = 57
    return "".join([chr(int(ord(os.urandom(1))/4.48) +65) for i in range(0,length)])
        
if __name__=="__main__":
    alice = Locksmith(5,23,6)
    bob = Locksmith(5,23,15)
    print(alice.makeIntermediateVal())
    #print(bob.makeKey(alice.makeIntermediateVal()))
    #print(alice.makeKey(bob.makeIntermediateVal()))
    #print(alice.makeIntermediateVal())
    #print(bob.makeIntermediateVal())
    v = VigLocksmith(5,23,"F")
    #print(v.makeIntermediateVal())
    v2= VigLocksmith(5,23,"O")
    print(v.makeKey(v2.makeIntermediateVal()))
    print(v2.makeKey(v.makeIntermediateVal()))
    
