import argparse
import os
import json
from typing import Any, Dict, List

import pandas as pd


RESULT_PREFIX = "r_"
DF_PATTERN = "{}_df.json"


def get_confusion_matrix(in_file: str) -> None:
    df = pd.DataFrame(columns=('fold', 'run', 'TP', 'FN', 'FP', 'TN', 'split'))
    for file_ in os.listdir(in_file):
        if file_.startswith(RESULT_PREFIX):
            split_ = file_.split('_')
            fold = int(split_[1].strip())
            run = int(split_[2].strip())
            conf_mat_file = os.path.join(in_file, file_, 'conf_mat.json')
            try:
                with open(conf_mat_file, 'r') as fd:
                    data = json.load(fd)
            except:
                print(f"Missing: {conf_mat_file}")
                continue
            for data_split in ('test', 'train'):
                conf_mat = eval(data[data_split])
                row = {
                    'fold': fold, 'run': run, 'split': data_split,
                    'TP': conf_mat[0][0], 'FN': conf_mat[0][1],
                    'FP': conf_mat[1][0], 'TN': conf_mat[1][1]
                       }
                df = df.append(row, ignore_index=True)

    with open(DF_PATTERN.format(in_file), 'w') as fd:
        json.dump(df.to_json(), fd)

        
def calculate_results(in_file: str) -> None:
    with open(DF_PATTERN.format(in_file), 'r') as fd:
        df = pd.read_json(json.load(fd))
        
    for data_split in ('test', 'train'):
        print(data_split)
        df_ = df[df['split'] == data_split]
        all_ex = df_[['TP', 'FN', 'FP', 'TN']].sum().sum()
        print(all_ex)
        for col in ('TP', 'FN', 'FP', 'TN'):
            sum_ = df_[col].sum()
            print(f"{col} {sum_}, {sum_ / all_ex:.3f}")

        acc = df_[['TP', 'TN']].sum().sum()
        print(f"Acc {acc}, {acc / all_ex:.3f}")


def main(in_files: List[str]) -> None:
    for in_file in in_files:
        print(in_file)
        if not os.path.exists(DF_PATTERN.format(in_file)):
            get_confusion_matrix(in_file)
        calculate_results(in_file)

if __name__ == '__main__':
        in_files = ('results')
        main(in_files)
