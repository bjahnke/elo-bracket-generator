Markup Install title below  
# ELO Simulator

Given a number of entities and their ELO rating, simulates matchups by calculating a win probablility using ELO and applying a random number generator to select a winner. 
After each round,
losers are eliminated and winners get updated ELO, matchups are processed until 1 team remains. 

A CSV table is output showing the teams remaining after each round, and their updated ELO scores.

# Requires:
- Python 3.6 or higher
- pip
- git

# Installation
After downloading the repository, navigate to the root folder and run the following command:
```bash
pip install -r requirements.txt
```

# Usage

```bash
python elo-sim.py --input <input_file> --output <output_file>
```
Input file is .json and output file is .csv, please include extensions. See sample-input-output folder for examples.

You can use the sample input file to test the program.

Windows
```bash
python elo-sim.py --input .\sample-input-output\teams.json --output .\sample-input-output\output.csv
```

Linux/Mac
```bash
python elo-sim.py --input ./sample-input-output/teams.json --output ./sample-input-output/output.csv
```