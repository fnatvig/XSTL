# XSTL: Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations

This repository contains code for reproducing the results reported in the paper:

**"Exploring Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations"** (Submitted to IEEE Access)

## Overview

This project investigates whether knowledge gained from one IEC 61850-based substation can be transferred to improve intrusion detection performance in another substation. The proposed method, called Cross-Substation Transfer Learning (XSTL), is a general framework that can be applied with any detection model. In this specific implementation, we use a simple unsupervised anomaly detector (autoencoder) to demonstrate and evaluate the approach across multiple dataset configurations.

## Folder structure

```
XSTL/
    ├── data/               # Preprocessed datasets 
    ├── src/                # Source code for XSTL implementation
    ├── results.txt         # Saved output metrics from experiments
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
Replace `[TEST]` with one of the test IDs defined in the paper (e.g., `A1`, `B2`, `D3`, etc). Depending on your hardware, this process may take several hours. 

## How to interpret the results
```bash
___Results_from_B2_FPR@TPR=1.0___
B2 FPR = 0.03244705662841683 +- 0.027510336687248692
B0 FPR = 0.08285287806698387 +- 0.039466704259132714
B2 p_value (FPR) = 6.57146445422408e-06 (l) - XSTL (B2) is better (STATISTICALLY SIGNIFICANT)
B2 AUC = 0.9999294402886972 +- 4.10544143732308e-05
B0 AUC = 0.9997274559964967 +- 0.0005110279168307987
B2 p_value (AUC) = 1.2983562924223692e-05 (r) - XSTL (B2) is better (STATISTICALLY SIGNIFICANT)
```







