# ONTlockDB
Simple password manager smart contract built on Ontology

## How to use
1) Store data (overwrites previous)

```
put(address, website, username, password)
```

Stores the `username` and `password` for `website` for the user with the wallet `address`.

2) Get data

```
get(address, website)
```

Gets the `username` and `password` for `website` for the user with the wallet `address`.

3) Delete data

```
delete(address, website)
```

Deletes the `username` and `password` for `website` for the user with the wallet `address`.
