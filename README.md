# ONTPassDB
Simple storage database built on Ontology

## How to use
1) Store data (overwrites previous)

```
put(key, val)
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

## Testing

Install dependencies with:
```
pip install -r requirements.txt
```

Run tests with
```
python -m unittest discover ONTPassTests/
```
