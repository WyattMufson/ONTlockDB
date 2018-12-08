from boa.interop.System.Runtime import Log
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.ExecutionEngine import GetCallingScriptHash
from boa.builtins import concat

ONTPASS = 'ONTPASS'
INVALID_ARGS = 'INVALID ARGUMENTS'
INVALID_FUNC = 'INVALID FUNCTION'


def Main(operation, args):
    ctx = GetContext()
    caller = GetCallingScriptHash()
    if operation == 'set':
        if len(args) == 2:
            key = args[0]
            val = args[1]
            return set(ctx, caller, key, val)
        Log(INVALID_ARGS)
    elif operation == 'get':
        if len(args) == 1:
            key = args[0]
            return get(ctx, caller, key)
        Log(INVALID_ARGS)
    elif operation == 'delete':
        if len(args) == 1:
            key = args[0]
            return delete(ctx, caller, key)
        Log(INVALID_ARGS)
    else:
        Log(INVALID_FUNC)
    return False


def getStorageKey(caller, key):
    prefix = concat(key, ONTPASS)
    storageKey = concat(prefix, caller)
    return storageKey


def set(ctx, caller, key, val):
    storageKey = getStorageKey(caller, key)
    Put(ctx, storageKey, val)
    return True


def get(ctx, caller, key):
    storageKey = getStorageKey(caller, key)
    return Get(ctx, storageKey)


def delete(ctx, caller, key):
    storageKey = getStorageKey(caller, key)
    Delete(ctx, storageKey)
    return True
