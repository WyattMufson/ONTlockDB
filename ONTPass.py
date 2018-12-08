from boa.interop.System.Runtime import Log, CheckWitness, Serialize, Deserialize
from boa.interop.System.Storage import GetContext, Get, Put
from boa.builtins import concat
ctx = GetContext()

ONTPASSDICT = 'ONTPASSDICT'
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


def getStorageDictKey(user):
    return concat(user, ONTPASSDICT)


def getStorageDict(user):
    storageDictKey = getStorageDictKey(user)
    serialized = Get(ctx, storageDictKey)
    if serialized:
        userDict = Deserialize(serialized)
        if userDict:
            return userDict

    return {}


def put(user, key, val):
    storageDict = getStorageDict(user)
    storageDict[key] = val
    serialized = Serialize(storageDict)
    storageDictKey = getStorageDictKey(user)
    Put(ctx, storageDictKey, serialized)
    return True


def get(user, key):
    storageDict = getStorageDict(user)
    item = storageDict[key]
    return item


def delete(user, key):
    deleted = put(user, key, "")
    return deleted


def find(user):
    storageDict = getStorageDict(user)
    serialized = Serialize(storageDict)
    return serialized
