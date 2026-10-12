# Dataset Card

## Primary dataset
UNSW-NB15 network intrusion detection dataset.

Official source:
https://research.unsw.edu.au/projects/unsw-nb15-dataset

## Expected schema
The supplied code expects CSV files containing `label` and `attack_cat`, plus predictor columns. Common UNSW-NB15 distributions provide predefined training and testing CSVs.

## Intended use
Educational model development, evaluation, and offline dataset replay.

## Out of scope
Live packet capture, production intrusion prevention, direct malware-file analysis, and guaranteed detection of unknown attacks.

## Data handling
The repository excludes raw dataset files by default. Download the data from the official source and check its terms before redistributing.
