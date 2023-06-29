import pandas as pd
import statistics
import pickle
import os
import csv

RESULT_PATH = './results/'


for root, dirs, files in os.walk(RESULT_PATH):
        # root: Current directory being scanned
        # dirs: Directories inside the current directory
        # files: Files inside the current directory
        if root == RESULT_PATH or "0_combined_pickle.pkl" in files:
            print(f"\nskipping{root}!\n")
            continue

        print(f"\n\nAdding from:{root}\ttotal files:{len(files)}\n\n")
        combined_df = pd.DataFrame()
        for i, file in enumerate(files):
            print(f"adding {i}/{len(files)}\tfrom: {root}")
            if ".csv" in file:
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                df['content'] = file  
                combined_df = pd.concat([combined_df,df], ignore_index=True)
        print("creating pickle")
        save_path = root + "/" + "0_combined_pickle.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(combined_df, f)

print("\n\nDONE\n")


RESULT_PATH = './response_times/'


for root, dirs, files in os.walk(RESULT_PATH):
        # root: Current directory being scanned
        # dirs: Directories inside the current directory
        # files: Files inside the current directory
        if root == RESULT_PATH or "0_combined_pickle.pkl" in files:
            print(f"\nskipping{root}!\n")
            continue

        print(f"\n\nAdding from:{root}\ttotal files:{len(files)}\n\n")
        combined_df = pd.DataFrame()
        for i, file in enumerate(files):
            print(f"adding {i}/{len(files)}\tfrom: {root}")
            if ".csv" in file:
                file_path = os.path.join(root, file)
                df = pd.read_csv(file_path)
                df['content'] = file  
                combined_df = pd.concat([combined_df,df], ignore_index=True)
        print("creating pickle")
        save_path = root + "/" + "0_combined_pickle.pkl"
        with open(save_path, 'wb') as f:
            pickle.dump(combined_df, f)

print("\n\nDONE\n")