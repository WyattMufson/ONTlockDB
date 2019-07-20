from ontology.interop.System.Runtime import Log, CheckWitness
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
ctx = GetContext()

ONTLOCK = 'ONTlockDB'


def Main(operation, args):
    if operation == 'put':
        Require(len(args) == 2)
        user = args[0]
        val = args[1]
        return put(user, val)
    elif operation == 'get':
        Require(len(args) == 1)
        user = args[0]
        return get(user)
    elif operation == 'delete':
        Require(len(args) == 1)
        user = args[0]
        return delete(user)
    return False


def getStorageKey(user):
    return concat(ONTLOCK, user) # pylint: disable=E0602


def put(user, val):
    RequireIsAddress(user)
    RequireWitness(user)
    storageKey = getStorageKey(user)
    Put(ctx, storageKey, val)
    return True


def get(user):
    RequireIsAddress(user)
    storageKey = getStorageKey(user)
    storage = Get(ctx, storageKey)
    if storage:
        return storage
    return ""


def delete(user):
    RequireIsAddress(user)
    RequireWitness(user)
    storageKey = getStorageKey(user)
    Delete(ctx, storageKey)
    return True


def RequireIsAddress(address):
    '''
    Raises an exception if the given address is not the correct length.

    :param address: The address to check.
    '''
    Require(len(address) == 20, "Address has invalid length")


def RequireWitness(address):
    '''
    Raises an exception if the given address is not a witness.

    :param address: The address to check.
    '''
    Require(CheckWitness(address), "Address is not witness")


def Require(expr, message="There was an error"):
    '''
    Raises an exception if the given expression is false.

    :param expr: The expression to evaluate.
    :param message: The error message to log.
    '''
    if not expr:
        Log(message)
        raise Exception(message)
