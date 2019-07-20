main="ONTlock"

if [ -f "src/$main.abi.json" ]; then
  rm src/$main.abi.json
fi

if [ -f "src/$main.avm" ]; then
  rm src/$main.avm
fi

if [ -f "src/$main.avm.str" ]; then
  rm src/$main.avm.str
fi

if [ -f "src/$main.debug.json" ]; then
  rm src/$main.debug.json
fi

if [ -f "src/$main.Func.Map" ]; then
  rm src/$main.Func.Map
fi

if [ -f "src/$main.warning" ]; then
  rm src/$main.warning
fi

if [ -d "src/ontology" ]; then
  rm -r src/ontology
fi
