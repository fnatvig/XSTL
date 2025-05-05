import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from keras.models import Sequential
from keras.layers import Dense, Input, Dropout
import tensorflow as tf
from joblib import Parallel, delayed
from scipy import integrate

def train(data, epochs, patience, lr):

    model = Sequential(
        [
        Input(shape=(len(data.columns), ),),
        Dropout(0.4),
        Dense(int(len(data.columns)), activation='relu'),
        Dropout(0.4),
        Dense(int(len(data.columns)*0.5), activation='relu'),
        Dropout(0.2),
        Dense(2, activation='relu', name='bottleneck'),
        Dense(int(len(data.columns)*0.5), activation='relu'),
        Dense(int(len(data.columns)), activation='relu', name='last_hidden'),
        Dense(len(data.columns), activation='sigmoid')
        ]
    )
    
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=patience, mode="min")
    opt = tf.keras.optimizers.Adam(learning_rate=lr)
    model.compile(optimizer=opt, loss='mae')
    
    history= model.fit(data.values, data.values, epochs=epochs, batch_size=256, callbacks=[early_stopping], shuffle=True, verbose=0)

    return model

def mse(arr1, arr2):
    mse = []
    for i in range(arr1.shape[0]):
        timestep_err = 0
        for j in range(arr1.shape[1]):
            timestep_err += (arr1[i][j]-arr2[i][j])*(arr1[i][j]-arr2[i][j])
        mse.append(timestep_err/arr1.shape[1])
    return np.array(mse)

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
    history= model.fit(data.values, data.values, epochs=epochs, batch_size=256, callbacks=[early_stopping], shuffle=True, verbose=0)
    
    if return_threshold:
        y_hat = model.predict(data.values, verbose=False)
        err = mse(y_hat, data.values)
        threshold = max(err)
        return model, threshold

    return model

def compute_tpr_fpr(threshold, err, true_indexes_set):
    """ Compute TPR and FPR for a given threshold. """
    tp, fp, fn, tn = 0, 0, 0, 0
    for i in range(len(err)):
        if err[i] >= threshold:
            if i in true_indexes_set:
                tp += 1
            else:
                fp += 1
        else:
            if i in true_indexes_set:
                fn += 1
            else:
                tn += 1
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    return threshold, fpr, tpr  # Returning threshold for sorting

def parallel_auc(err, true_indexes_array, thresholds, n_jobs=-1):
    """ Compute AUC using parallelization over thresholds. """
    true_indexes_set = set(true_indexes_array)  # Convert to set for faster lookup

    # Parallel computation
    results = Parallel(n_jobs=n_jobs)(
        delayed(compute_tpr_fpr)(threshold, err, true_indexes_set) for threshold in thresholds
    )

    # Sorting by threshold in descending order (to match original reverse logic)
    results.sort(reverse=True, key=lambda x: x[0])
    
    # Extract sorted FPR and TPR values
    fpr = [res[1] for res in results]
    tpr = [res[2] for res in results]

    # Compute AUC using trapezoidal integration
    return integrate.trapezoid(y=tpr, x=fpr)

def reconstruct_auc(prepared_df, data, model1, model2, num_thresholds):
    y_hat1 = model1.predict(prepared_df.values, verbose=False)
    err1 = mse(y_hat1, prepared_df.values)

    y_hat2 = model2.predict(prepared_df.values, verbose=False)
    err2 = mse(y_hat2, prepared_df.values)

    temp = data[data.loc[:, "label"]].index
    true_indexes_array = temp.to_numpy(dtype='int')

    thresholds = np.linspace(0, max([*err1, *err2]), num_thresholds)

    auc1 = parallel_auc(err1, true_indexes_array, thresholds)
    auc2 = parallel_auc(err2, true_indexes_array, thresholds)
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

def reconstruct_sensitive(data, data_raw, model1, model2):
    y_hat1 = model1.predict(data.values, verbose=False)
    err1 = mse(y_hat1, data.values)

    y_hat2 = model2.predict(data.values, verbose=False)
    err2 = mse(y_hat2, data.values)

    temp = data_raw[data_raw.loc[:, "label"]].index
    true_indexes_array = temp.to_numpy(dtype='int')

    fpr1 = get_fpr(err1, true_indexes_array)
    fpr2 = get_fpr(err2, true_indexes_array)
    
    return fpr1, fpr2