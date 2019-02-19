# Census11

Sample project for building a post-strat sheet.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

This assumes you manage python versions with `pyenv` as outlined [here](https://github.com/pyenv/pyenv) and virtual environments with `pyenv-virtualenv` as outlined [here](https://github.com/pyenv/pyenv-virtualenv).

See `.python-version` for the python version required.

See `requirements.txt` for the libraries required.

### Setup Virtual Environment:

Manage python versions with `pyenv`. Check python versions installed include version specified in 
`.python-version` (i.e. :
```
$ pyenv versions
```

Manage virtual environments with `pyenv-virtualenvs`. Create a virtual environment:
```
$ pyenv virtualenv 3.7.2 census11
```

### Install Dependencies:

CD into folder to activate the virtual environment and run:
```
$ pip install requirements.txt
```

## Run from Command Line
```
$ python create_ps_sheet_from_mlsoa.py
$ python constituency_level_data.py
```

## Data used
Currently we use the following data:
- output/constituencies_england_wales.csv
- output/census_11_four_way_joint_distribution.csv
- output/earnings_15_by_constituency.csv
- output/hanretty_constituency_data_2011.csv
- output/2010_results_england_wales_by_constituency.csv
- output/2015_results_england_wales_by_constituency.csv
