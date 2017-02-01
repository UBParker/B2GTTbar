# pyttbarfw


##Recipe for running semi-leptonic ttbar selection (type1 - fully merged tops: AK8 is top candidate) on B2G2016 V4 TTrees:

```
./type1_commands.csh
```
##Recipe for running semi-leptonic ttbar selection (type2 - partially merged tops: AK8 is W candidate) on B2G2016 V4 TTrees:

```
./type2_commands.csh
```

##Recipe for plotting files from above:

NOTE: plotstack.py is written in python 3.4
main differences  2.7  -> 3.4 : 
- print “” -> print(“”)
- xrange() -> range()

### Type 1 and Type 2
```
./plotcommands.csh
```
