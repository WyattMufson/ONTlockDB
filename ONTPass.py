from boa.interop.System.Runtime import Log
from boa.interop.Storage import GetContext, Get, Put

def Main(operation, args):
  if operation == 'Hello':
    msg = args[0]
    return Hello(msg)

  return False


def Hello(msg):
  Notify(msg)
  return True
      