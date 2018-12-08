# ONTPassDB
Simple storage database built on Ontology

## How to use
1) Store data (overwrites previous)

```
set(key, val)
```

Sets the value for `key` to be equal to `val`

2) Get data

```
get(key)
```

Gets the value for `key`

3) Delete data

```
delete(key)
```

Delete the value for `key`

4) Find data

```
find()
```

Returns a list of keys that can be looked up
