from boa.interop.System.Runtime import Log, CheckWitness
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.builtins import concat
ctx = GetContext()

ONTPASSITEM = 'ONTPASSITEM'
ONTPASSLIST = 'ONTPASSLIST'
INVALID_ARGS = 'INVALID ARGUMENTS'
INVALID_FUNC = 'INVALID FUNCTION'
INVALID_USER = 'INVALID USER'


def Main(operation, args):
    if operation == 'put':
        if len(args) == 3:
            user = args[0]
            if len(user) == 20:
                if CheckWitness(user):
                    key = args[1]
                    val = args[2]
                    return put(user, key, val)
                Log(INVALID_USER)
        Log(INVALID_ARGS)
    elif operation == 'get':
        if len(args) == 2:
            user = args[0]
            if len(user) == 20:
                key = args[1]
                return get(user, key)
            Log(INVALID_USER)
        Log(INVALID_ARGS)
    elif operation == 'delete':
        if len(args) == 2:
            user = args[0]
            if len(user) == 20:
                if CheckWitness(user):
                    key = args[1]
                    return delete(user, key)
                Log(INVALID_USER)
        Log(INVALID_ARGS)
    elif operation == 'find':
        if len(args) == 1:
            user = args[0]
            if len(user) == 20:
                return find(user)
            Log(INVALID_USER)
        Log(INVALID_ARGS)
    else:
        Log(INVALID_FUNC)
    return False


def getStorageItemKey(user, key):
    prefix = concat(user, ONTPASSITEM)
    storageItemKey = concat(prefix, key)
    return storageItemKey


def put(user, key, val):
    storageItemKey = getStorageItemKey(user, key)
    Put(ctx, storageItemKey, val)
    return True


def get(user, key):
    storageItemKey = getStorageItemKey(user, key)
    val = Get(ctx, storageItemKey)
    return val


def delete(user, key):
    storageItemKey = getStorageItemKey(user, key)
    Delete(ctx, storageItemKey)
    return True


def find(user):
    # lst = getStorageList(caller)
    return True
