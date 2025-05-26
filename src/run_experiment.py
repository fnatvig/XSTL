import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

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

    # df_pretrain = df_pretrain.loc[:int(len(df_pretrain)/10)].reset_index(drop=True)
    # df_train = df_train.loc[:int(len(df_train)/10)].reset_index(drop=True)
    # df_test = df_test.loc[:int(len(df_test)/100)].reset_index(drop=True)
    return df_pretrain, df_train, df_test 


def preprocess_data(df_pretrain, df_train, df_test, wnd_size):

    df_pretrain = preprocess_df(df_pretrain, wnd_size)
    df_train = preprocess_df(df_train, wnd_size)
    df_test = preprocess_df(df_test, wnd_size)

    df1 = pd.concat([df_pretrain], axis=0).reset_index(drop=True)
    df = pd.concat([df_train], axis=0).reset_index(drop=True)

    df_pretrain = (df_pretrain - df1.mean())/(df1.std())
    df_pretrain = df_pretrain.fillna(0.0)

    df_train = (df_train - df.mean())/(df.std())
    df_train = df_train.fillna(0.0)    
    
    df_test = (df_test - df.mean())/(df.std())
    df_test = df_test.fillna(0.0)
    
    return df_pretrain, df_train, df_test

def test_hypothesis(fpr_a, fpr_b, auc_a, auc_b, test, ablation):
    arr_a = np.array(fpr_a)
    arr_b = np.array(fpr_b)

    # Constructing ID string for baseline (given the ID of test)
    baseline = ""
    freezing = ""
    if ablation:
        letter = ""
        if test[0]=="E":
            letter="A"
        elif test[0]=="F":
            letter="B"
        elif test[0]=="G":
            letter="C"
        elif test[0]=="H":
            letter="D"
        freezing = letter + test[1]
    else:
        baseline = test[0]+"0"

    # Performing wilcoxon signed-rank test (both tails)
    alternative = "greater"
    result1 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
    alternative = "less"
    result2 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
    
    # Writing results to stdout
    print("\n")
    print(f"___Results_from_{test}___")
    stat_sign = ""
    if (result1.pvalue<0.05) or (result2.pvalue<0.05):
        stat_sign = "(STATISTICALLY SIGNIFICANT)"
    if ablation:
        print(f"{freezing} (FPR@TPR=1) FPR = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"{test} (FPR@TPR=1) FPR = {np.mean(arr_b)} +- {np.std(arr_b)}")
    else:
        print(f"{test} (FPR@TPR=1) FPR = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"{baseline} (FPR@TPR=1) FPR = {np.mean(arr_b)} +- {np.std(arr_b)}")
    if result2.pvalue<result1.pvalue:
        if ablation:
            print(f"{test} (FPR@TPR=1) p_value = {result2.pvalue} (l) - Freezing ({freezing}) is better {stat_sign}")
        else:
            print(f"{test} (FPR@TPR=1) p_value = {result2.pvalue} (l) - XSTL ({test}) is better {stat_sign}")
    else:
        if ablation:
            print(f"{test} (FPR@TPR=1) p_value = {result1.pvalue} (r) - Non-freezing ({test}) is better {stat_sign}")
        else:
            print(f"{test} (FPR@TPR=1) p_value = {result1.pvalue} (r) - Baseline ({baseline}) is better {stat_sign}")

    # Do the same as above but this time for AUC
    arr_a = np.array(auc_a)
    arr_b = np.array(auc_b)
    alternative = "greater"
    result1 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
    alternative = "less"
    result2 = wilcoxon(arr_a, arr_b, alternative=alternative, method='approx')
    stat_sign = ""
    if (result1.pvalue<0.05) or (result2.pvalue<0.05):
        stat_sign = "(STATISTICALLY SIGNIFICANT)"
    if ablation:
        print(f"{freezing} (AUC-ROC) AUC = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"{test} (AUC-ROC) AUC = {np.mean(arr_b)} +- {np.std(arr_b)}")
    else:
        print(f"{test} (AUC-ROC) AUC = {np.mean(arr_a)} +- {np.std(arr_a)}")
        print(f"{baseline} (AUC-ROC) AUC = {np.mean(arr_b)} +- {np.std(arr_b)}")
    if result2.pvalue<result1.pvalue:
        if ablation:
            print(f"{test} (AUC-ROC) p_value = {result2.pvalue} (l) - Non-freezing ({test}) is better {stat_sign}")
        else:
            print(f"{test} (AUC-ROC) p_value = {result2.pvalue} (l) - Baseline ({baseline}) is better {stat_sign}")
    else:
        if ablation:
            print(f"{test} (AUC-ROC) p_value = {result1.pvalue} (r) - Freezing ({freezing}) is better {stat_sign}")
        else:
            print(f"{test} (AUC-ROC) p_value = {result1.pvalue} (r) - XSTL ({test}) is better {stat_sign}")


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
    for i in range(1,31):
        print(f"\rRound: {i}/30", end='', flush=True)
        
        # Training model A
        model_a = train(data=df_pretrain, epochs=1000, patience=3, lr= 0.001)
        model_a = retrain(data=df_train, model=model_a, epochs=1000, patience=5, trainable_encoder=False, lr= 0.003)
        model_a = retrain(data=df_train, model=model_a, epochs=1000, patience=3, trainable_encoder=True, lr= 0.0003)
        
        # Training model B
        model_b = None
        if ablation:
            model_b = train(data=df_pretrain, epochs=1000, patience=3, lr=0.001)
            model_b = retrain(data=df_train, model=model_b, epochs=1000, patience=5, trainable_encoder=True, lr=0.003)
        else: 
            model_b = train(data=df_train, epochs=1000, patience=5, lr= 0.003)
        model_b = retrain(data=df_train, model=model_b, epochs=1000, patience=3, trainable_encoder=True, lr= 0.0003)

        # Evaluate model A and model B
        fpr_a, fpr_b, auc_a, auc_b = detect(df_test, df_test_raw, model_a=model_a, model_b=model_b, tpr_target=[1.0])
        
        # Save results
        fpr_A.append(fpr_a)
        fpr_B.append(fpr_b)
        auc_A.append(auc_a)
        auc_B.append(auc_b)
    
    # Statistical evaluation and comparison
    test_hypothesis(fpr_A, fpr_B, auc_A, auc_B, args.test, ablation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run XSTL transfer learning experiment")
    parser.add_argument('--test', type=str, required=True, help='Insert test number (see table X and Y in paper).', choices=[
        "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "D3", 
        "E1", "E2", "E3", "F1", "F2", "F3", "G1", "G2", "G3", "H1", "H2", "H3"])

    args = parser.parse_args()
    main(args)
