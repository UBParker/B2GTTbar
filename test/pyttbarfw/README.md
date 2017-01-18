# pyttbarfw


##Recipe for running semi-leptonic ttbar selection (type1) on B2G2016 V4 TTrees:

```
./RunSemiLepTTbar_commands-type1.sh
```
##Recipe for running semi-leptonic ttbar selection (type2) on B2G2016 V4 TTrees:

```
./RunSemiLepTTbar_commands-type2.sh
```

##Recipe for plotting files from above:

NOTE: B2GSelectionPlotter is written in python 3.4
main differences  2.7  -> 3.4 : 
- print “” -> print(“”)
- xrange() -> range()

### Type 1
```
python B2GSelectionPlotter.py 
```
### Type 2
```
python B2GSelectionPlotter.py --Type2
```
