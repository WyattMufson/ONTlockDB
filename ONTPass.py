from boa.interop.System.Runtime import Log, Serialize, Deserialize
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.ExecutionEngine import GetCallingScriptHash
from boa.builtins import concat

ONTPASSITEM = 'ONTPASSITEM'
ONTPASSLIST = 'ONTPASSLIST'
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
    elif operation == 'find':
        if len(args) == 0:
            return find(ctx, caller)
    else:
        Log(INVALID_FUNC)
    return False


def getStorageList(ctx, caller):
    storageListKey = concat(caller, ONTPASSLIST)
    lst = Get(ctx, storageListKey)
    if lst:
        return Deserialize(lst)
    else:
        return []


def indexOf(lst, item):
    length = len(lst)
    for i in range(length):
        j = lst[i]
        if j == item:
            return i
    return -1


def saveList(ctx, caller, lst):
    storageListKey = concat(caller, ONTPASSLIST)
    serialzed = Serialize(lst)
    Put(ctx, storageListKey, serialzed)
    return True


def addToStorageList(ctx, caller, key):
    lst = getStorageList(ctx, caller)
    index = indexOf(lst, key)
    if index != -1:
        return True
    else:
        lst.append(key)
        saved = saveList(ctx, caller, lst)
        return saved


def getStorageItemKey(caller, key):
    prefix = concat(caller, ONTPASSITEM)
    storageItemKey = concat(prefix, key)
    return storageItemKey


def set(ctx, caller, key, val):
    storageItemKey = getStorageItemKey(caller, key)
    Put(ctx, storageItemKey, val)
    return True


def get(ctx, caller, key):
    storageItemKey = getStorageItemKey(caller, key)
    return Get(ctx, storageItemKey)


def delete(ctx, caller, key):
    storageItemKey = getStorageItemKey(caller, key)
    Delete(ctx, storageItemKey)
    return True


def find(ctx, caller):
    lst = getStorageList(ctx, caller)
    return lst
