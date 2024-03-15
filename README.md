# README for Text Analyser Application

## Overview

The Text Analyser application is a command-line tool designed to perform detailed text analysis using the OpenAI API. It leverages GPT-based models to extract themes, entities, sentiment, and other insights from text inputs, generating concise reports. This tool is ideal for data scientists, researchers, or anyone looking to derive meaningful analysis from textual data.

## Features

- **Text Analysis:** Generate detailed reports from text inputs, highlighting key insights and patterns.
- **Customizable Models:** Uses the OpenAI API with the flexibility to specify different GPT models.
- **Report Sections:** The generated reports include an introduction, key insights, text analysis findings (such as sentiment analysis, topic modeling, entity recognition, readability level, and a textual heatmap of most popular tokens), and a summary.

## Requirements

- Python 3.8+
- OpenAI Python package
- Typer package for CLI interactions
- An OpenAI API key set as an environment variable (`OPENAI_API_KEY`).

## Installation

Before running the application, ensure you have Python installed on your system and the required packages:

```bash
pip install -r requirements.txt
```

## Configuration

Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY='your_openai_api_key_here'
```

Make sure to replace `your_openai_api_key_here` with your actual API key.

## Usage

To use the Text Analyser, run the following command from the terminal, replacing `path_to_your_text_file.txt` with the path to the text file you want to analyze:

```bash
docker run -e OPENAI_API_KEY='your_openai_api_key_here' text-analyser "$(cat path_to_your_text_file.txt)"
```

## Docker

The application is designed to be run as a Docker container. Ensure you have Docker installed and running on your system. Build the Docker image using the Dockerfile provided in the source repository:

```bash
docker build -t text-analyser .
```

## Running the Application

After building the Docker image, you can analyze a text file as follows:

```bash
docker run -e OPENAI_API_KEY='your_openai_api_key_here' text-analyser "$(cat path_to_your_text_file.txt)"
```

## Limitations

- The analysis quality is dependent on the model selected and the input text.
- Ensure that your OpenAI API key has sufficient credits and permissions for the operations you intend to perform.


## Assumptions

- To minimise number of calls to OpenAI API, only one call is performed for a given text


## Testing

- For testing, please run the following command:

```bash
python -m unittest tests.py
```

