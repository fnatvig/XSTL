# XSTL: Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations

This repository contains code and experiment scripts for the paper:

**"Exploring Cross-Substation Transfer Learning for Improving Cybersecurity in IEC 61850 Substations"** (Submitted to IEEE Access)

## Overview

This project investigates whether knowledge gained from one IEC 61850-based substation can be transferred to improve intrusion detection performance in another substation. The proposed method, called Cross-Substation Transfer Learning (XSTL), is a general framework that can be applied with any detection model. In this specific implementation, we use a simple unsupervised anomaly detector (autoencoder) to demonstrate and evaluate the approach across multiple dataset configurations.

The main contributions include:
- Pretraining and fine-tuning an IDS on IEC 61850 traffic from different substations
- Evaluation based on two threshold selection strategies: high-sensitivity (ensuring recall = 1) and AUC-based (assessing overall trade-off)
- Statistical comparison using the Wilcoxon signed-rank test to account for training variability
- An ablation study assessing the impact of freezing pretrained layers

## Getting started

It is recommended to use a virtual environment. You can do this manually or simply run the provided batch script:

Double-click the file `setup_venv.bat` to automatically:
- Create a virtual environment in a folder called `venv`
- Activate it
- Install all required packages from `requirements.txt`

