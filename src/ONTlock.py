from ontology.interop.System.Runtime import Log, CheckWitness, Serialize
from ontology.interop.System.Storage import GetContext, Get, Put, Delete
ctx = GetContext()

ONTLOCK_ENTRY = 'ONTlockDB-ENTRY-KEY'


def Main(operation, args):
    if operation == 'put':
        Require(len(args) == 4)
        address = args[0]
        website = args[1]
        username = args[2]
        password = args[3]
        return put(address, website, username, password)
    elif operation == 'get':
        Require(len(args) == 2)
        address = args[0]
        website = args[1]
        return get(address, website)
    elif operation == 'delete':
        Require(len(args) == 2)
        address = args[0]
        website = args[1]
        return delete(address, website)
    return False


def put(address, website, username, password):
    RequireIsAddress(address)
    RequireWitness(address)
    RequireShorterThan(website, 65)
    RequireShorterThan(username, 65)
    RequireShorterThan(password, 65)
    return do_put(address, website, username, password)


def get(address, website):
    RequireIsAddress(address)
    RequireShorterThan(website, 65)
    return do_get(address, website)


def delete(address, website):
    RequireIsAddress(address)
    RequireWitness(address)
    RequireShorterThan(website, 65)
    return do_delete(address, website)


def do_put(address, website, username, password):
    storageKey = getStorageKey(address, website)
    entry = {"username": username, "password": password}
    Put(ctx, storageKey, Serialize(entry))
    return True


def do_get(address, website):
    storageKey = getStorageKey(address, website)
    storage = Get(ctx, storageKey)
    if storage is not None:
        return storage
    return ""


def do_delete(address, website):
    storageKey = getStorageKey(address, website)
    Delete(ctx, storageKey)
    return True

# Helpers

def getStorageKey(address, website):
    '''
    Creates a unique storage key for the given address and website.

    :param address: The user's address.
    :param website: The website to store information for.
    '''
    return concat(concat(ONTLOCK_ENTRY, address), website) # pylint: disable=E0602


def RequireShorterThan(string, length):
    '''
    Raises an exception if the string's length exceeds the limit.

    :param string: The string to check.
    :param length: The length limit.
    '''
    Require(len(string) < length, "String is too long")


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
