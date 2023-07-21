# Handling Apple Health data

Current state - generate CSV file containing only Weight - BodyMass

## Installation

```sh
pip install -r requirements.txt
```

## Usage

Export the Apple Health data and upload to your Mac.

Extract the archive and place [apple_health_export](apple_health_export) 
folder in the project folder.

Run:

```sh
python fetch_body_mass.py
```

The result is placed in 
[apple_health_export/BodyMass.csv](apple_health_export/BodyMass.csv)
