# XSTL: Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations

This repository contains code and experiment scripts for the paper:

**"Exploring Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations"** (Submitted to IEEE Access)

## Overview

This project investigates whether knowledge gained from one IEC 61850-based substation can be transferred to improve intrusion detection performance in another substation. The proposed method, called Cross-Substation Transfer Learning (XSTL), is a general framework that can be applied with any detection model. In this specific implementation, we use a simple unsupervised anomaly detector (autoencoder) to demonstrate and evaluate the approach across multiple dataset configurations.

The main contributions include:
- Pretraining and fine-tuning an IDS on IEC 61850 traffic from different substations
- Results are evaluated under two operating points: FPR@TPR=1.0 and AUC-ROC.
- Statistical comparison using the Wilcoxon signed-rank test to account for training variability
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

Once the virtual environment is activated and the required packages are installed, you can run a full experiment by executing one of the experiment scripts.

For example, to run the main set of XSTL experiments (Table 6 in the paper):

```bash
python experiments/run_all.py
```


