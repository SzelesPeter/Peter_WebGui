from time import *
from threading import *

def HandleMsg( arg1, arg2 ) :
  print(arg1, arg2)

def HandleAnotherMsg( arg1, arg2, arg3 ) :
  print (arg1, arg2, arg3)

def DestinationThread() :
  while True :
    if len(q)>0:
        items = q.pop()
        func = items[0]
        args = items[1:]
        func(*args)

q = []
q.append([HandleMsg, "a", "b"])
q.append([HandleAnotherMsg, "c", "d", "e"])
q.append([HandleMsg, "e", "f"])

thred_1=Thread(target=DestinationThread)
thred_1.start()

