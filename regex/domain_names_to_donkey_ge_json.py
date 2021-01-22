import math
import random
import json

import pandas as pd


# TODO could use some built in scikit fuctions probably...
def main():
    train_test_ratio = 0.7
    donkey_ge_data = {"train": {"inputs": [], "outputs": []}, "test": {"inputs": [], "outputs": []},}
    in_file = 'regex/domain_names/small_domain_names.json'
    out_file = 'regex/domain_names/data_set_small_domain_names.json'
    malign_column_name = 'Cybox_key_value'
    malign_df = pd.read_json(in_file)
    malign_data = malign_df[malign_column_name]
    in_file = 'regex/domain_names/benign_alexa_domain_names.json'
    with open(in_file, 'r') as fd:
        benign_data = json.load(fd)

    for i, data in enumerate((benign_data, malign_data)):
        random.shuffle(data)
        n_data = len(data)
        n_train = math.ceil(n_data * train_test_ratio)
        n_test = n_data - n_train
        assert (n_train + n_test) == n_data, f"{n_train} {n_test} {n_data}"
        donkey_ge_data["train"]["inputs"].extend(data[:n_train])
        donkey_ge_data["train"]["outputs"].extend([i] * n_train)
        donkey_ge_data["test"]["inputs"].extend(data[n_train:])
        donkey_ge_data["test"]["outputs"].extend([i] * n_test)

    print(donkey_ge_data)
    with open(out_file, "w") as fd:
        json.dump(donkey_ge_data, fd)

    
if __name__ == '__main__':
    main()
