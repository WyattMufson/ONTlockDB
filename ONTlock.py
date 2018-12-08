from boa.interop.System.Runtime import Log, CheckWitness
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.builtins import concat
ctx = GetContext()

ONTLOCK = 'ONTlockDB'
INVALID_ARGS = 'INVALID ARGUMENTS'
INVALID_FUNC = 'INVALID FUNCTION'
INVALID_USER = 'INVALID USER'


def Main(operation, args):
    if operation == 'put':
        if len(args) == 2:
            user = args[0]
            if len(user) == 20:
                if CheckWitness(user):
                    val = args[1]
                    return put(user, val)
                Log(INVALID_USER)
        Log(INVALID_ARGS)
    elif operation == 'get':
        if len(args) == 1:
            user = args[0]
            if len(user) == 20:
                return get(user)
            Log(INVALID_USER)
        Log(INVALID_ARGS)
    elif operation == 'delete':
        if len(args) == 1:
            user = args[0]
            if len(user) == 20:
                if CheckWitness(user):
                    return delete(user)
                Log(INVALID_USER)
        Log(INVALID_ARGS)
    else:
        Log(INVALID_FUNC)
    return False


def getStorageKey(user):
    return concat(user, ONTLOCK)


def put(user, val):
    storageKey = getStorageKey(user)
    Put(ctx, storageKey, val)
    return True


def get(user):
    storageKey = getStorageKey(user)
    storage = Get(ctx, storageKey)
    if storage:
        return storage
    else:
        return ""


def delete(user):
    storageKey = getStorageKey(user)
    Delete(ctx, storageKey)
    return True
