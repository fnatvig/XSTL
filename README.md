# XSTL: Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations

This repository contains code for reproducing the results reported in the paper:

**"Exploring Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations"** (Submitted to IEEE Access)

## Overview

This project investigates whether knowledge gained from one IEC 61850-based substation can be transferred to improve intrusion detection performance in another substation. The proposed method, called Cross-Substation Transfer Learning (XSTL), is a general framework that can be applied with any detection model. In this specific implementation, we use a simple unsupervised anomaly detector (autoencoder) to demonstrate and evaluate the approach across multiple dataset configurations.

## Folder structure

```
XSTL/
    ├── data/               # Datasets 
    ├── src/                # Source code for XSTL implementation
    ├── requirements.txt    # List of dependencies for the project
    ├── setup_venv.bat      # Script for creating a virtual environment (Windows)
    └── README.md           # Project overview and usage instructions
```

## Getting started

It is recommended to use a virtual environment before running any experiments.

### Windows (recommended)

Double-click the file `setup_venv.bat` to:
- Create a virtual environment in a folder called `venv`
- Activate it
- Install all required packages from `requirements.txt`

### macOS/Linux (manual setup)

If you're not on Windows, run the following from the command line:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running experiments

Once the virtual environment is generated and the required packages are installed, you're ready for running experiments. 

### Windows (recommended)
To reproduce the result of an experiment, open a command prompt and run:
```bash 
venv\Scripts\activate.bat  # If not already activated
python -B src/run_experiment.py --test [TEST] 
```
Replace `[TEST]` with one of the test IDs defined in the paper (e.g., `A1`, `B2`, `D3`, etc). Depending on your hardware, this process may take several hours. 

### macOS/Linux
To reproduce the result of an experiment, open a terminal and run:
```bash
source venv/bin/activate  # If not already activated
python -B src/run_experiment.py --test [TEST] 
```
Replace `[TEST]` with one of the test IDs defined in the paper (e.g., `A1`, `B2`, `D3`, etc). Depending on your hardware, this process may take a few hours. 

## How to interpret the results
To reproduce any of the results reported in Table 6, run one of the following tests: `A1`-`A3`, `B1`-`B3`, `C1`-`C3` or `D1`-`D3`. The text below reveals the output from running test `A1`. The first 
```bash
___Results_from_A1___
A1 (FPR@TPR=1) FPR = 0.0329321765090027 +- 0.02521485260047171
A0 (FPR@TPR=1) FPR = 0.05395092825823305 +- 0.012494693195758974
A1 (FPR@TPR=1) p_value = 0.0006586774211924253 (l) - XSTL (A1) is better (STATISTICALLY SIGNIFICANT)
A1 (AUC-ROC) AUC = 0.9999085333913132 +- 6.583640955529369e-05
A0 (AUC-ROC) AUC = 0.9998750624711353 +- 4.2074750687536923e-05
A1 (AUC-ROC) p_value = 0.0376066561077384 (r) - XSTL (A1) is better (STATISTICALLY SIGNIFICANT)
```

```bash
___Results_from_E1___
A1 (FPR@TPR=1) FPR = 0.0329321765090027 +- 0.02521485260047171
E1 (FPR@TPR=1) FPR = 0.043996641477749794 +- 0.022888771065752732
E1 (FPR@TPR=1) p_value = 0.05659532941705212 (l) - Freezing (A1) is better
A1 (AUC-ROC) AUC = 0.9999085333913132 +- 6.583640955529369e-05
E1 (AUC-ROC) AUC = 0.9999052780495591 +- 5.7444726019119126e-05
E1 (AUC-ROC) p_value = 0.35944378106813346 (r) - Freezing (A1) is better
```





