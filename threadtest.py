import threading
import time
import sys
import select


bool promptShowing = False

def printSomething(something="hi"):
    looped = 0
    while True:
        looped+=1
        sys.stdout.write(something+str(looped))
        sys.stdout.flush()
        time.sleep(10)

def takeAndPrint():
    while True:
        x = input("Enter anything: ")
        

thread1 = threading.Thread(target=printSomething)
thread2 = threading.Thread(target=takeAndPrint)


thread2.start()
thread1.start()
