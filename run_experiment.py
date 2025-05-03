import pandas as pd
import argparse

def parse_test(test):
    X_pretrain = None
    threshold_approach = None
    ablation = None
    match test:
        case "A1":
            X_pretrain = "01-normal.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "A2":
            X_pretrain = "02-normal.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "A3":
            X_pretrain = "03-normal.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "B3":
            X_pretrain = "UnderFrequency.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = False 
        case "C3":
            X_pretrain = "UnderFrequency.xlsx"
            threshold_approach = "High-sensitivity" 
            ablation = True 
    return X_pretrain, threshold_approach, ablation

def import_data(X_pretrain):
    df_pretrain = pd.read_excel("data/"+X_pretrain)
    df_train = pd.read_excel("data/02-normal.xlsx")
    df_test = pd.read_excel("data/15-attack.xlsx")
    df_test = df_test.loc[:int(len(df_test)/100)].reset_index(drop=True)
    return df_pretrain, df_train, df_test 

def preprocess_data(df_pretrain, df_train, df_test, wnd_size):
    df_source_prepared = preprocess_df(df_source, wnd_size)
    df_source2_prepared = preprocess_df(df_source2, wnd_size)
    df_target_prepared = preprocess_df(df_target, wnd_size)

def main(args):
    print(f"Running Test: {args.test}")
    X_pretrain, threshold_approach, ablation = parse_test(args.test)
    
    print(f"Reading data. This could take a while...")
    df_pretrain, df_train, df_test = import_data(X_pretrain)

    print(f"Preprocessing data. This will take even longer...")
    df_pretrain, df_train, df_test = import_data(X_pretrain)

    print(df_pretrain.head())
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run XSTL transfer learning experiment")
    parser.add_argument('--test', type=str, required=True, help='Insert test number (see table 3 in paper).', choices=[
        "A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "B1", "B2", "B3", "B4", "B5", "B6", "C1", "C2", "C3", "C4", "C5", "C6"])

    args = parser.parse_args()
    main(args)
