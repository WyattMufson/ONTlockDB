from boa.interop.System.Runtime import Log, Serialize, Deserialize
from boa.interop.System.Storage import GetContext, Get, Put, Delete
from boa.interop.System.ExecutionEngine import GetCallingScriptHash
from boa.builtins import concat
ctx = GetContext()

ONTPASSITEM = 'ONTPASSITEM'
ONTPASSLIST = 'ONTPASSLIST'
INVALID_ARGS = 'INVALID ARGUMENTS'
INVALID_FUNC = 'INVALID FUNCTION'


def Main(operation, args):
    caller = GetCallingScriptHash()
    if operation == 'put':
        if len(args) == 2:
            key = args[0]
            val = args[1]
            return put(caller, key, val)
        Log(INVALID_ARGS)
    elif operation == 'get':
        if len(args) == 1:
            key = args[0]
            return get(caller, key)
        Log(INVALID_ARGS)
    elif operation == 'delete':
        if len(args) == 1:
            key = args[0]
            return delete(caller, key)
        Log(INVALID_ARGS)
    elif operation == 'find':
        if len(args) == 0:
            return find(caller)
    else:
        Log(INVALID_FUNC)
    return False


def getStorageList(caller):
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


def saveList(caller, lst):
    storageListKey = concat(caller, ONTPASSLIST)
    serialzed = Serialize(lst)
    Put(ctx, storageListKey, serialzed)
    return True


def addToStorageList(caller, key):
    lst = getStorageList(caller)
    index = indexOf(lst, key)
    if index != -1:
        return True
    else:
        lst.append(key)
        saved = saveList(caller, lst)
        return saved


def removeFromStorageList(caller, key):
    lst = getStorageList(caller)
    index = indexOf(lst, key)
    if index == -1:
        return True
    else:
        del lst[index]
        saved = saveList(caller, lst)
        return saved


def getStorageItemKey(caller, key):
    prefix = concat(caller, ONTPASSITEM)
    storageItemKey = concat(prefix, key)
    return storageItemKey


def put(caller, key, val):
    storageItemKey = getStorageItemKey(caller, key)
    Put(ctx, storageItemKey, val)
    added = addToStorageList(caller, key)
    return added


def get(caller, key):
    storageItemKey = getStorageItemKey(caller, key)
    return Get(ctx, storageItemKey)


def delete(caller, key):
    storageItemKey = getStorageItemKey(caller, key)
    Delete(ctx, storageItemKey)
    removed = removeFromStorageList(caller, key)
    return removed


def find(caller):
    lst = getStorageList(caller)
    return lst
