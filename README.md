# Biomedical Graph Database

## Overview

This project uses Hetionet biomedical data to explore relationships between diseases, drugs, genes, and anatomy. I built the project in Python using Kùzu as a graph database and RocksDict to store query results.

The project also includes both a graphical interface and a command-line interface for interacting with the data.

## What I Did

For this project, I:

* Loaded Hetionet nodes and relationships into a Kùzu graph database
* Created relationships between diseases, compounds, genes, and anatomy
* Used graph queries to retrieve biomedical relationships
* Stored query results using RocksDict for easier access
* Built a Tkinter interface for running the queries
* Added a command-line option for running the same queries without the GUI

## Queries

The project includes two main queries.

### Disease Lookup

The first query allows the user to enter a disease ID and retrieve information associated with that disease, including:

* Drugs
* Genes
* Anatomical locations

### Compound-Disease Relationships

The second query searches for compound-disease pairs connected through gene and anatomy relationships while excluding compound-disease relationships that already exist in the dataset.

## Technologies

* Python
* Kùzu
* RocksDict
* pandas
* Tkinter
* Hetionet

## Files

* `main.py` - Runs the GUI or command-line interface and displays query results
* `import_data.py` - Loads the Hetionet data, builds the graph database, and generates query results
* `constants.py` - Defines database paths, node types, and relationship types
* `.gitignore` - Excludes datasets, generated databases, virtual environments, and cache files

## Data

This project uses Hetionet data stored in `nodes.tsv` and `edges.tsv`. These dataset files are not included in this repository.

The graph includes four main types of biomedical entities:

* Anatomy
* Compounds
* Diseases
* Genes

## Running the Project

The project uses Python along with Kùzu, RocksDict, and pandas.

Install the required packages:

```bash
pip install kuzu pandas rocksdict
```

After adding the Hetionet `nodes.tsv` and `edges.tsv` files to the project directory, build the databases by running:

```bash
python import_data.py
```

To open the graphical interface:

```bash
python main.py
```

Or run the command-line version:

```bash
python main.py cli
```

## About the Project

This project was completed as part of Big Data Technology course. The goal was to work with biomedical network data using graph and key-value databases and build an interface for querying the results.
