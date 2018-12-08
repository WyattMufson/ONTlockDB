from boa.interop.System.Runtime import Log, CheckWitness, Serialize, Deserialize
from boa.interop.System.Storage import GetContext, Get, Put
from boa.builtins import concat
ctx = GetContext()

ONTPASSDICT = 'ONTPASSDICT'
ONTPASSSET = 'ONTPASSSET'
ONTPASSARRAY = 'ONTPASSARRAY'
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


def getHasStored(user, key):
    prefix = concat(user, ONTPASSSET)
    hasStoredKey = concat(prefix, key)
    hasStored = Get(ctx, hasStoredKey)
    if hasStored:
        return hasStored
    else:
        return False


def keyList(user):
    listKey = concat(user, ONTPASSARRAY)
    lst = Get(ctx, listKey)
    if lst:
        return Deserialize(lst)
    else:
        return []


def addToList(user, key):
    listKey = concat(user, ONTPASSARRAY)
    listKey.append(key)
    serialized = Serialize(listKey)
    Put(ctx, listKey, serialized)
    return True


def didStore(user, key, stored):
    prefix = concat(user, ONTPASSSET)
    hasStoredKey = concat(prefix, key)
    Put(ctx, hasStoredKey, stored)
    if stored:
        added = addToList(user, key)
        return added
    return True


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
    stored = didStore(user, key, True)
    return stored


def get(user, key):
    storageDict = getStorageDict(user)
    stored = getHasStored(user, key)
    if stored:
        item = storageDict[key]
        return item
    else:
        return ""


def delete(user, key):
    deleted = put(user, key, "")
    stored = didStore(user, key, False)
    if stored:
        return deleted
    else:
        return False


def find(user):
    storageDict = getStorageDict(user)
    serialized = Serialize(storageDict)
    return serialized
