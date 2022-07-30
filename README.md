# Funda Analysis

The goal of this project is to get data from funda.nl and do some analysis of it.

## Description

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

Amsterdam dependency: price / built date
