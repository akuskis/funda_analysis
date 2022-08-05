# Funda Analysis

## Description

Analysis of house pricing in the Netherlands by data received from [Funda](htts://funda.nl).

## Setup

Get [conda](https://conda.io) into your system.
The commands below will import the environment and activate it.

```shell
conda env create -f environment.yml
conda activate funda
```

## Pulling data

Call the following command from repository to pull data from [Funda](https://funda.nl):

```shell
cd scrapy
scrapy crawl funda -O dump.json
```

Where `funda` is a name of the spider and `dump.json` is a place where to store collected data.

## Historical data

## Analysis

Run [JupyterLab](https://jupyter.org/) and navigate to the analysis folder (JupyterLab is installed as part of environment):

```shell
jupyter-lab
```

### Overview

Show boxplot of price distribution:

```shell
./analysis/overview.py PATH_TO_DUMP_FILE
```
