import math
import random
import json
import re

import pandas as pd


def parse_top_thousand_alexa_ed():
    in_file = 'regex/domain_names/ed_https_htmlstrip.com_alexa-top-1000-most-visited-websites.html'
    # TODO such a hack...
    alexa_thousand = []
    with open(in_file, 'r') as fd:
        for line in fd:
            split_ = line.split('> ')
            if len(split_) == 2:
                alexa_thousand.append(split_[1][:-7])

    out_file = 'regex/domain_names/benign_kilo_alexa_domain_names.json'    
    with open(out_file, 'w') as fd:
        json.dump(alexa_thousand, fd)
                
# TODO could use some built in scikit fuctions probably...
def main():
    label_balance = True
    train_test_ratio = 0.7
    donkey_ge_data = {"train": {"inputs": [], "outputs": []}, "test": {"inputs": [], "outputs": []},}
    in_file = 'regex/domain_names/domainNames.json'
    out_file = 'regex/domain_names/data_set_kilo_domain_names.json'
    malign_column_name = 'Cybox_key_value'
    malign_df = pd.read_json(in_file)
    malign_data = malign_df[malign_column_name]
    in_file = 'regex/domain_names/benign_kilo_alexa_domain_names.json'
    with open(in_file, 'r') as fd:
        benign_data = json.load(fd)

    if label_balance:
        max_size = min(len(benign_data), len(malign_data))
    else:
        max_size = max(len(benign_data), len(malign_data))
    print(max_size)
    for i, data in enumerate((benign_data, malign_data)):
        data = data[:max_size]
        random.shuffle(data)
        n_data = len(data)
        n_train = math.ceil(n_data * train_test_ratio)
        n_test = n_data - n_train
        assert (n_train + n_test) == n_data, f"{n_train} {n_test} {n_data}"
        donkey_ge_data["train"]["inputs"].extend(data[:n_train])
        donkey_ge_data["train"]["outputs"].extend([i] * n_train)
        donkey_ge_data["test"]["inputs"].extend(data[n_train:])
        donkey_ge_data["test"]["outputs"].extend([i] * n_test)

    print(len(donkey_ge_data["train"]["inputs"]))
    with open(out_file, "w") as fd:
        json.dump(donkey_ge_data, fd)

    
if __name__ == '__main__':
    #parse_top_thousand_alexa_ed()
    main()

