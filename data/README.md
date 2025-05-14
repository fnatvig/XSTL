# Data Directory

This folder is used to store the datasets used in the XSTL experiments.

## Source Datasets

The data is derived from two publicly available research projects:

1. **A synthesized dataset for cybersecurity study of IEC 61850 based substation**: Biswas, P. P., Tan, H. C., Zhu, Q., Li, Y., Mashima, D., & Chen, B. (2019, October). A synthesized dataset for cybersecurity study of IEC 61850 based substation. In 2019 IEEE International Conference on Communications, Control, and Computing Technologies for Smart Grids (SmartGridComm) (pp. 1-7). IEEE. Link to data: https://github.com/smartgridadsc/IEC61850SecurityDataset

2. **PowerDuck: A GOOSE data set of cyberattacks in substations**: Zemanek, S., Hacker, I., Wolsing, K., Wagner, E., Henze, M., & Serror, M. (2022, August). PowerDuck: A GOOSE data set of cyberattacks in substations. In Proceedings of the 15th Workshop on Cyber Security Experimentation and Test (pp. 49-53). Link to data: https://zenodo.org/records/6974112

Please refer to the original publications for details on how the datasets were generated and licensed.

## Modifications

The only modification made to the original files is the conversion of network trace logs and annotations to `.xlsx` format to simplify preprocessing and improve compatibility with this implementation. No content has been altered.

## File Naming Convention

The files in this folder follow the naming used in the main paper:
- `Daa.xlsx`, `Dab.xlsx`, ..., `Dae.xlsx`

These correspond to network traces during different substation conditions used for training, pretraining, and testing.
