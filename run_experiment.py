import tensorflow as tf
import numpy as np
import random
import os
import pandas as pd
import argparse


from scipy.stats import wilcoxon
from sklearn.metrics import roc_auc_score

from preprocessing import *
from autoencoder import *

# Set seeds
seed = 42
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

# Optional: Force deterministic ops (TensorFlow 2.9+)
os.environ['TF_DETERMINISTIC_OPS'] = '1'

def parse_test(test):
    X_pretrain = None
    X_train = None
    ablation = False
    match test:
        case "A1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "01-normal.xlsx" 
        case "A2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "01-normal.xlsx" 
        case "A3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "01-normal.xlsx" 
        case "B1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "02-normal.xlsx" 
        case "B2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "02-normal.xlsx" 
        case "B3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "02-normal.xlsx" 
        case "C1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "03-normal.xlsx" 
        case "C2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "03-normal.xlsx" 
        case "C3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "03-normal.xlsx" 
        case "D1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "04-normal.xlsx" 
        case "D2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "04-normal.xlsx" 
        case "D3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "04-normal.xlsx" 
        case "E1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "01-normal.xlsx" 
            ablation = True
        case "E2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "01-normal.xlsx" 
            ablation = True
        case "E3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "01-normal.xlsx" 
            ablation = True
        case "F1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "02-normal.xlsx" 
            ablation = True
        case "F2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "02-normal.xlsx" 
            ablation = True
        case "F3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "02-normal.xlsx" 
            ablation = True
        case "G1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "03-normal.xlsx" 
            ablation = True
        case "G2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "03-normal.xlsx" 
            ablation = True
        case "G3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "03-normal.xlsx" 
            ablation = True
        case "H1":
            X_pretrain = "BusbarProtection.xlsx"
            X_train = "04-normal.xlsx" 
            ablation = True
        case "H2":
            X_pretrain = "BreakFailure.xlsx"
            X_train = "04-normal.xlsx" 
            ablation = True
        case "H3":
            X_pretrain = "UnderFrequency.xlsx"
            X_train = "04-normal.xlsx" 
            ablation = True
    
    return X_pretrain, X_train, ablation


def import_data(X_pretrain, X_train):
    df_pretrain = pd.read_excel("data/"+X_pretrain)
    df_train = pd.read_excel("data/"+X_train)
    df_test = pd.read_excel("data/15-attack.xlsx")
    return df_pretrain, df_train, df_test 


def preprocess_data(df_pretrain, df_train, df_test, wnd_size):

    df_pretrain = preprocess_df(df_pretrain, wnd_size)
    df_train = preprocess_df(df_train, wnd_size)
    df_test = preprocess_df(df_test, wnd_size)

    df_pretrain = df_pretrain.drop("wnd_goose_num_of_same_dest", axis=1)
    df_pretrain = df_pretrain.drop("wnd_goose_num_of_all_dest", axis=1) 
    df_train = df_train.drop("wnd_goose_num_of_same_dest", axis=1)
    df_train = df_train.drop("wnd_goose_num_of_all_dest", axis=1) 
    df_test = df_test.drop("wnd_goose_num_of_same_dest", axis=1)
    df_test = df_test.drop("wnd_goose_num_of_all_dest", axis=1) 

    df1 = pd.concat([df_pretrain], axis=0).reset_index(drop=True)
    df = pd.concat([df_train], axis=0).reset_index(drop=True)

    df_pretrain = (df_pretrain - df1.mean())/(df1.std())
    df_pretrain = df_pretrain.fillna(0.0)

    df_train = (df_train - df.mean())/(df.std())
    df_train = df_train.fillna(0.0)    
    
    df_test = (df_test - df.mean())/(df.std())
    df_test = df_test.fillna(0.0)
    
    return df_pretrain, df_train, df_test

def test_hypothesis(fpr_a, fpr_b, auc_a, auc_b, test):
    arr_a = np.array(fpr_a)
    arr_b = np.array(fpr_b)
    if not (arr_a==arr_b).all():
        diff = arr_a-arr_b
        alternative = "greater"
        result1 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
        alternative = "less"
        result2 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
        print("\n")
        print(f"___Results_from_{test}_TPR=1.0___")
        if (result1.pvalue<0.05) or (result2.pvalue<0.05):
            print("STATISTICALLY SIGNIFICANT")
        print(f"XSTL FPR = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"Baseline FPR = {np.mean(arr_b)} +- {np.std(arr_b)}")
        # print(f"difference in FPR = {np.mean(diff)} +- {np.std(diff)}")
        if result2.pvalue<result1.pvalue:
            print(f"p_value = {result2.pvalue} (l) - XSTL is better")
        else:
            print(f"p_value = {result1.pvalue} (r) - Baseline is better")
        print("\n")
    else:
        print(f"___Results_from_{test}_TPR=1.0___")
        print("No difference in FPR")

    arr_a = np.array(auc_a)
    arr_b = np.array(auc_b)
    if not (arr_a==arr_b).all():
        diff = arr_a-arr_b
        alternative = "greater"
        result1 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
        alternative = "less"
        result2 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
        print("\n")
        print(f"___Results_from_{test}_AUC-ROC___")
        if (result1.pvalue<0.05) or (result2.pvalue<0.05):
            print("STATISTICALLY SIGNIFICANT")
        print(f"XSTL AUC = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"Baseline AUC = {np.mean(arr_b)} +- {np.std(arr_b)}")
        if result2.pvalue<result1.pvalue:
            print(f"p_value = {result2.pvalue} (l) - Baseline is better")
        else:
            print(f"p_value = {result1.pvalue} (r) - XSTL is better")
        print("\n")
    else:
        print(f"___Results_from_{test}_AUC-ROC___")
        print("No difference in AUC-ROC")

def main(args):
    print(f"Running Test: {args.test}")
    X_pretrain, X_train, ablation = parse_test(args.test)
    
    print(f"Reading data. This could take a while...")
    df_pretrain, df_train, df_test_raw = import_data(X_pretrain, X_train)

    print(f"Preprocessing data. This will take even longer...")
    df_pretrain, df_train, df_test = preprocess_data(df_pretrain, df_train, df_test_raw, 2)

    auc_A = []
    auc_B = []
    fpr_A = []
    fpr_B = []
    for i in range(30):
        print(f"Round: {i}", flush=True)
        

        model_a = train(data=df_pretrain, epochs=1000, patience=3, lr= 0.001)
        model_a = retrain(data=df_train, model=model_a, epochs=1000, patience=5, trainable_encoder=False, lr= 0.003)
        model_a = retrain(data=df_train, model=model_a, epochs=1000, patience=3, trainable_encoder=True, lr= 0.0003)
        
        model_b = None
        if ablation:
            model_b = train(data=df_pretrain, epochs=1000, patience=3, lr=0.001)
            model_b = retrain(data=df_train, model=model_b, epochs=1000, patience=5, trainable_encoder=True, lr=0.003)
        else: 
            model_b = train(data=df_train, epochs=1000, patience=5, lr= 0.003)
        model_b = retrain(data=df_train, model=model_b, epochs=1000, patience=3, trainable_encoder=True, lr= 0.0003)

        fpr_a, fpr_b, auc_a, auc_b = detect(df_test, df_test_raw, model_a=model_a, model_b=model_b, tpr_target=[1.0])
        fpr_A.append(fpr_a)
        fpr_B.append(fpr_b)
        auc_A.append(auc_a)
        auc_B.append(auc_b)
            
        print(f"fpr_p = {fpr_a}")
        print(f"fpr_t = {fpr_b}")
        print(f"auc_p = {auc_a}")
        print(f"auc_t = {auc_b}")
    
    test_hypothesis(fpr_A, fpr_B, auc_A, auc_B, args.test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run XSTL transfer learning experiment")
    parser.add_argument('--test', type=str, required=True, help='Insert test number (see table X and Y in paper).', choices=[
        "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "D3", 
        "E1", "E2", "E3", "F1", "F2", "F3", "G1", "G2", "G3", "H1", "H2", "H3"])

    args = parser.parse_args()
    main(args)
