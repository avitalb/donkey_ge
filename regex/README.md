# TODO 

- Refactor to use `argparse` for running and analysing experiments. Will make it more modular and useable
- Run static analysis and style scripts, e.g. `black`

# RegExp experiments

Run an experiment. 
```
time python regex/experiments.py > tmp.out 2> tmp.err
 ```
 
Analyse result data. 
 ```
python regex/analyse_results.py
```
