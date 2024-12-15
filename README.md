# Automated Data Analysis with LLM Assistance

## Project Overview

This Python-based project automates data analysis by utilizing Large Language Model (LLM) assistance to provide meaningful insights. The tool can process CSV files, generate visualizations (correlation heatmaps and distribution plots), and offer an AI-driven narrative that explains patterns and trends in the data. All findings are compiled into a well-structured Markdown report for easy sharing.

## Features

- **Automated Data Exploration**: Automatically loads a CSV dataset and provides a summary of the data structure, data types, missing values, and summary statistics.
- **Correlation Heatmap**: Generates a heatmap to visualize correlations between numerical columns in the dataset.
- **Distribution Plots**: Automatically creates distribution plots for numerical columns to understand their distributions.
- **LLM-Assisted Narrative**: Uses a Large Language Model (GPT) to generate a narrative that summarizes the dataset, points out key trends, and suggests insights.
- **Markdown Report**: Compiles the analysis results, including the dataset summary, LLM narrative, and visualizations, into a comprehensive Markdown report.

## Installation

### Requirements

- Python 3.7+
- `pandas`: for data manipulation
- `seaborn`: for visualization
- `matplotlib`: for plotting
- `requests`: for API requests (for interacting with the LLM)
- `chardet`: for automatic encoding detection
- `argparse`: for handling command-line arguments

To install the required dependencies, you can use the following command:

```bash
pip install pandas seaborn matplotlib requests chardet argparse
