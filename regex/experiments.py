import multiprocessing
import copy
import os
import random
import json
from typing import Any, Dict, List

from sklearn.model_selection import KFold
import yaml

from heuristics.donkey_ge import run as donkey_run


def create_data_sets(in_file, n_folds: int=10):
    with open(in_file, 'r') as fd:
        data = json.load(fd)

    X = []
    y = []
    for split_ in data.keys():
        X += data[split_]["inputs"]
        y += data[split_]["outputs"]

    order = random.sample(range(len(X)), len(X))
    X = [X[_] for _ in order]
    y = [y[_] for _ in order]
    assert len(X) == len(y)
    kf = KFold(n_splits=n_folds)
    for i, (train, test) in enumerate(kf.split(X)):
        out_file = in_file.replace('.json', f"_fold_{i}.json")
        print(out_file)
        donkey_ge_data = {"train": {"inputs": [], "outputs": []}, "test": {"inputs": [], "outputs": []},}
        donkey_ge_data["train"]["inputs"] = [X[_] for _ in train]
        donkey_ge_data["train"]["outputs"] = [y[_] for _ in train]
        donkey_ge_data["test"]["inputs"] = [X[_] for _ in test]
        donkey_ge_data["test"]["outputs"] = [y[_] for _ in test]
        with open(out_file, "w") as fd:
            json.dump(donkey_ge_data, fd)

            
def create_configurations(in_file, n_folds):
    with open(in_file, 'r') as fd:
        org_settings: Dict[str, Any] = yaml.load(fd, Loader=yaml.FullLoader)

    for i in range(n_folds):
        settings = copy.deepcopy(org_settings)
        settings['seed'] = i
        out_file = settings['fitness_function']['exemplars'].replace('.json', f"_fold_{i}.json")
        settings['fitness_function']['exemplars'] = out_file
        cfg_file = in_file.replace('.yaml', f'_fold_{i}.yaml')
        print(cfg_file)
        with open(cfg_file, 'w') as fd:
            yaml.dump(settings, fd)
            

def evaluate_run(args : List[str]) -> str:
    donkey_run(args)
    return f'DONE {args}'


def main(in_file: str, n_runs: int, n_folds: int) -> None:
    NOVELTY SEARCH
    configs = []
    os.makedirs("results", exist_ok=True)
    for i in range(n_folds):
        fold_cfg = in_file.replace('.yaml', f'_fold_{i}.yaml')
        with open(fold_cfg, 'r') as fd:
            org_config = yaml.load(fd, Loader=yaml.FullLoader)

        for j in range(n_runs):
            config = copy.deepcopy(org_config)
            config["seed"] = config.get("seed", 1) + j
            config["output_dir"] = f"results/r_{i}_{j}"
            configs.append(config)
            
    # Evaluate runs
    with multiprocessing.Pool(processes = multiprocessing.cpu_count()) as pool:
        res = pool.map_async(evaluate_run, configs)
        results = res.get()
        assert len(configs) == len(results)
        print(results)

if __name__ == '__main__':
    n_folds = 10
    n_runs = 10
    create_data_sets('regex/domain_names/data_set_kilo_domain_names.json', n_folds)
    create_configurations('regex/domain_names/domain_names.yaml', n_folds)
    main('regex/domain_names/domain_names.yaml', n_runs, n_folds)
