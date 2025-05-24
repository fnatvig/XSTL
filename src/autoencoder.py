import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Input, Dropout
import tensorflow as tf
from joblib import Parallel, delayed
from scipy import integrate
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

def train(data, epochs, patience, lr):

    model = Sequential(
        [
        Input(shape=(len(data.columns), ),),
        # Dense(int(len(data.columns)*4), activation='relu'),
        # Dropout(0.4),
        # Dense(int(len(data.columns)*3), activation='relu'),
        # Dropout(0.4),
        # Dense(int(len(data.columns)*2), activation='relu'),
        # Dropout(0.4),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dropout(0.1),
        Dense(16, activation='relu'),
        Dropout(0.1),
        Dense(8, activation='relu'),
        Dropout(0.1),
        Dense(2, activation='relu', name='bottleneck'),
        Dropout(0.1),
        Dense(8, activation='relu'),
        Dropout(0.1),
        Dense(16, activation='relu'),
        Dropout(0.1),
        Dense(32, activation='relu'),
        Dropout(0.1),

        # Dense(int(len(data.columns)*2), activation='relu', name='last_hidden'),
        # Dense(int(2*len(data.columns)*3), activation='relu', name='last_last_hidden'),
        # Dense(int(2*len(data.columns)*4), activation='relu', name='last_last_last_hidden'),
        Dense(len(data.columns), activation='linear')
        ]
    )
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=patience, mode="min")
    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=opt, loss='mae')
    
    history= model.fit(data.values, data.values, epochs=epochs, batch_size=32, callbacks=[early_stopping], shuffle=True, verbose=0)

    return model

def mse(arr1, arr2):
    return np.mean((arr1 - arr2) ** 2, axis=1)

def retrain(data, model, epochs, patience, trainable_encoder, lr, return_threshold=False):
    if not trainable_encoder:
        bottleneck_index = None
        for i, layer in enumerate(model.layers):
            if layer.name == 'bottleneck':
                bottleneck_index = i
                break
        if bottleneck_index is None:
            raise ValueError("Layer 'bottleneck' not found in the model.")
        for i in range(len(model.layers[:bottleneck_index+1])):
            model.layers[i].trainable = False
    else:
        bottleneck_index = None
        for i, layer in enumerate(model.layers):
            if layer.name == 'bottleneck':
                bottleneck_index = i
                break
        if bottleneck_index is None:
            raise ValueError("Layer 'bottleneck' not found in the model.")
        for i in range(len(model.layers[:bottleneck_index+1])):
            model.layers[i].trainable = True

    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=patience, mode="min")
    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=opt, loss='mae')
    history= model.fit(data.values, data.values, epochs=epochs, batch_size=32, callbacks=[early_stopping], shuffle=True, verbose=0)
    
    if return_threshold:
        y_hat = model.predict(data.values, verbose=False)
        err = mse(y_hat, data.values)
        threshold = max(err)
        return model, threshold

    return model

def reconstruct_auc(prepared_df, data, model1, model2, num_thresholds):
    y_hat1 = model1.predict(prepared_df.values, verbose=False)
    err1 = mse(y_hat1, prepared_df.values)

    y_hat2 = model2.predict(prepared_df.values, verbose=False)
    err2 = mse(y_hat2, prepared_df.values)
    
    auc1 = roc_auc_score(data.loc[:,"label"], err1)
    auc2 = roc_auc_score(data.loc[:,"label"], err2)
    
    return auc1, auc2

def get_threshold(err, true_indexes_array):
    return np.min(err[true_indexes_array])

def get_fpr(err, true_indexes_array):
    threshold = get_threshold(err, true_indexes_array)
    tp, fp, fn, tn = 0, 0, 0, 0
    for i in range(len(err)):
        if err[i] >= threshold:
            if i in true_indexes_array:
                tp+=1
            else:
                fp+=1
        else:
            if i in true_indexes_array:
                fn+=1
            else:
                tn+=1
    return fp/(fp+tn)

def get_fpr_at_fixed_tpr(y_true, y_score, tpr_targets=[1.0, 0.95], tolerance=1e-4):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    results = []

    for tpr_target in tpr_targets:
        mask = tpr >= (tpr_target - tolerance)
        if not any(mask):
            # results[tpr_target] = {'fpr': None, 'threshold': None}
            results.append(None)
        else:
            best_idx = mask.nonzero()[0][fpr[mask].argmin()]
            results.append(fpr[best_idx])
    return results

def get_tpr_at_fixed_fpr(y_true, y_score, fpr_targets=[0.05], tolerance=1e-4):
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    results = []

    for fpr_target in fpr_targets:
        # Find indices where FPR is just below or equal to the target (within tolerance)
        mask = fpr <= (fpr_target + tolerance)
        if not any(mask):
            results.append(None)
        else:
            best_idx = mask.nonzero()[0][-1]  # max TPR under FPR constraint
            results.append(tpr[best_idx])
    return results

def detect(data, data_raw, model_a, model_b, tpr_target):
    y_hat1 = model_a.predict(data.values, verbose=False)
    err1 = mse(y_hat1, data.values)

    y_hat2 = model_b.predict(data.values, verbose=False)
    err2 = mse(y_hat2, data.values)

    fpr_a = get_fpr_at_fixed_tpr(data_raw.loc[:,"label"], err1, tpr_target)
    fpr_b = get_fpr_at_fixed_tpr(data_raw.loc[:,"label"], err2, tpr_target)

    auc_a = roc_auc_score(data_raw.loc[:,"label"], err1)
    auc_b = roc_auc_score(data_raw.loc[:,"label"], err2)

    return fpr_a[0], fpr_b[0], auc_a, auc_b
    

def reconstruct_sensitive(data, data_raw, model1, model2, tpr_target, fpr_target):
    y_hat1 = model1.predict(data.values, verbose=False)
    err1 = mse(y_hat1, data.values)

    y_hat2 = model2.predict(data.values, verbose=False)
    err2 = mse(y_hat2, data.values)

    temp = data_raw[data_raw.loc[:, "label"]].index
    true_indexes_array = temp.to_numpy(dtype='int')

    # fpr1 = get_fpr(err1, true_indexes_array)
    # fpr2 = get_fpr(err2, true_indexes_array)

    results1 = get_fpr_at_fixed_tpr(data_raw.loc[:,"label"], err1, tpr_target)
    results2 = get_fpr_at_fixed_tpr(data_raw.loc[:,"label"], err2, tpr_target)

    results3 = get_tpr_at_fixed_fpr(data_raw.loc[:,"label"], err1, fpr_target)
    results4 = get_tpr_at_fixed_fpr(data_raw.loc[:,"label"], err2, fpr_target)

    auc1 = roc_auc_score(data_raw.loc[:,"label"], err1)
    auc2 = roc_auc_score(data_raw.loc[:,"label"], err2)

    print("AUC_diff = ", auc1-auc2)

    return results1, results2, results3, results4