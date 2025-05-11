import pandas as pd


a = pd.DataFrame([[1,2],[3,4]], columns=["A", "B"])

a.to_excel("data/a.xlsx", index=False)
# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from sklearn.metrics import roc_curve

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from sklearn.metrics import roc_curve

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# from sklearn.metrics import roc_curve


# def get_threshold(err, true_indexes_array):
#     return np.min(err[true_indexes_array])

# def get_fpr_at_threshold(err, labels, threshold):
#     tp, fp, fn, tn = 0, 0, 0, 0
#     for i in range(len(err)):
#         if err[i] >= threshold:
#             if labels[i]:
#                 tp += 1
#             else:
#                 fp += 1
#         else:
#             if labels[i]:
#                 fn += 1
#             else:
#                 tn += 1
#     return fp / (fp + tn) if (fp + tn) > 0 else None, tp / (tp + fn) if (tp + fn) > 0 else None

# def reconstruct_sensitive(df):
#     err = df["reconstruction_error"].values
#     labels = df["label"].values

#     thresholds_to_try = sorted(np.unique(err))[::-1]

#     results = {}
#     tpr_targets = [1.0, 0.99, 0.98, 0.97, 0.96, 0.95]

#     # Initialize best FPRs for each TPR target
#     for tpr_target in tpr_targets:
#         results[tpr_target] = None

#     # For each threshold, compute FPR and TPR
#     for threshold in thresholds_to_try:
#         fpr, tpr = get_fpr_at_threshold(err, labels, threshold)
#         for tpr_target in tpr_targets:
#             if tpr is not None and tpr >= tpr_target:
#                 if results[tpr_target] is None or fpr < results[tpr_target]:
#                     results[tpr_target] = fpr

#     return results

# def get_fpr_at_fixed_tpr(y_true, y_score, tpr_targets=[1.0, 0.95], tolerance=1e-6):
#     fpr, tpr, thresholds = roc_curve(y_true, y_score)
#     results = {}

#     for tpr_target in tpr_targets:
#         mask = tpr >= (tpr_target - tolerance)
#         if not any(mask):
#             results[tpr_target] = {'fpr': None, 'threshold': None}
#         else:
#             best_idx = mask.nonzero()[0][fpr[mask].argmin()]
#             print(thresholds[best_idx])
#             results[tpr_target] = {
#                 'fpr': fpr[best_idx],
#                 'threshold': thresholds[best_idx]
#             }

#     return results

# np.random.seed(42)

# # Normal traffic: centered around 0.6, with some variance
# normal_errors = np.random.normal(loc=0.3, scale=0.05, size=50)
# normal_errors = np.clip(normal_errors, 0, 1)

# # Attack traffic: mostly lower, but some overlap with normal
# attack_errors = np.random.normal(loc=0.55, scale=0.1, size=500)
# attack_errors = np.clip(attack_errors, 0, 1)

# # Combine into DataFrame
# df_test = pd.DataFrame({
#     'label': np.array([False] * len(normal_errors) + [True] * len(attack_errors)),
#     'reconstruction_error': np.concatenate([normal_errors, attack_errors])
# })

# y_true = df_test['label'].astype(int).values
# y_score = df_test['reconstruction_error'].values

# # fpr_a = reconstruct_sensitive(df)
# fpr_b = get_fpr_at_fixed_tpr(y_true, y_score, tpr_targets=[1.0, 0.99, 0.98])

# # print("FPR from reconstruct_sensitive:")
# # print(fpr_a)
# print("\nFPR from find_high_sensitivity_threshold_from_df:")
# print(fpr_b)

# attack_data = df_test[df_test["label"] == True]
# normal_data = df_test[df_test["label"] == False]

# plt.figure(figsize=(10, 4))
# plt.scatter(normal_data.index, normal_data["reconstruction_error"], color='blue', label='Normal', alpha=0.7)
# plt.scatter(attack_data.index, attack_data["reconstruction_error"], color='red', label='Attack', alpha=0.7)

# plt.xlabel("Sample index")
# plt.ylabel("Reconstruction error")
# plt.title("Reconstruction Error for Normal and Attack Samples")
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

# # def get_threshold(err, true_indexes_array):
# #     return np.min(err[true_indexes_array])


# # def get_fpr(err, true_indexes_array):
# #     threshold = get_threshold(err, true_indexes_array)
# #     tp, fp, fn, tn = 0, 0, 0, 0
# #     for i in range(len(err)):
# #         if err[i] >= threshold:
# #             if i in true_indexes_array:
# #                 tp+=1
# #             else:
# #                 fp+=1
# #         else:
# #             if i in true_indexes_array:
# #                 fn+=1
# #             else:
# #                 tn+=1
# #     return fp/(fp+tn)

# # def reconstruct_sensitive(df):

# #     temp = df[df.loc[:, "label"]].index
# #     true_indexes_array = temp.to_numpy(dtype='int')

# #     fpr = get_fpr(df.loc[:, "reconstruction_error"], true_indexes_array)
    
# #     return fpr

# # def find_high_sensitivity_threshold_from_df(df, tpr_target=1.0, tolerance=1e-8):
# #     """
# #     Finds the threshold on reconstruction error that achieves TPR >= tpr_target with the lowest FPR.
    
# #     Parameters:
# #         df: pandas.DataFrame
# #             Must contain 'label' (0 for normal, 1 for attack) and 'reconstruction_error' columns.
# #         tpr_target: float, default=1.0
# #             The desired minimum true positive rate.
# #         tolerance: float, default=1e-8
# #             Numerical tolerance when comparing TPR to target.

# #     Returns:
# #         best_threshold: float or None
# #             Threshold that gives TPR >= tpr_target and minimizes FPR.
# #         best_fpr: float or None
# #             False positive rate at the selected threshold.
# #     """
# #     if 'label' not in df.columns or 'reconstruction_error' not in df.columns:
# #         raise ValueError("DataFrame must contain 'label' and 'reconstruction_error' columns.")
    
# #     y_true = df['label'].values
# #     y_score = df['reconstruction_error'].values  # higher = more anomalous

# #     fpr, tpr, thresholds = roc_curve(y_true, y_score)

# #     mask = tpr >= (tpr_target - tolerance)

# #     if not np.any(mask):
# #         return None, None

# #     best_idx = np.argmin(fpr[mask])
# #     best_threshold = thresholds[mask][best_idx]
# #     best_fpr = fpr[mask][best_idx]

# #     return best_threshold, best_fpr

# # # Data
# # # Example DataFrame
# # np.random.seed(42)  # for reproducibility

# # # 80 normal samples: lower reconstruction errors, some noise
# # normal_errors = np.random.normal(loc=0.2, scale=0.05, size=80)
# # normal_errors = np.clip(normal_errors, 0, 1)  # keep in [0, 1]

# # # 20 attack samples: higher reconstruction errors, some overlap
# # attack_errors = np.random.normal(loc=0.4, scale=0.1, size=20)
# # attack_errors = np.clip(attack_errors, 0, 1)

# # # Create DataFrame
# # df = pd.DataFrame({
# #     'label': np.array([False] * 80 + [True] * 20),  # 0 = normal, 1 = attack
# #     'reconstruction_error': np.concatenate([normal_errors, attack_errors])
# # })



# # fpr_a = reconstruct_sensitive(df)
# # best_threshold, fpr_b = find_high_sensitivity_threshold_from_df(df)

# # print(fpr_a)
# # print(fpr_b)




