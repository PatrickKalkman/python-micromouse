# python-micromouse
This repository contains all the source code and examples from the article [How to Simulate the Micromouse Competition With Python](https://itnext.io/how-to-simulate-the-micromouse-competition-with-python-ce29254edd2e)

![Mouse](/mouse.jpg "Mouse")

## Setup and Installation

### Installing Poetry

This project uses Poetry for dependency management. Poetry is a tool for Python application management that handles setting up virtual environments and simplifying package management.

To install Poetry:

- **For UNIX and MacOS users**, run the following command in your terminal:

```bash
curl -sSL https://install.python-poetry.org | python - 
```

**For Windows users**, use PowerShell to install Poetry with this command:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Setting up the Project

1. **Clone the repository**: Use `git clone` to clone this repository to your local machine.

2. **Navigate to the project directory**: Change your current working directory to the cloned repository's location.

3. **Install Dependencies**: Install the project's dependencies with Poetry by running `poetry install` in the project's root directory. Poetry will read the `pyproject.toml` file and set up a new virtual environment with all the necessary dependencies.

## Running the Application

1. **Activate the Poetry shell**: Activate the virtual environment that Poetry has set up by running `poetry shell`. Your command line prompt should change to show that you are in a new shell environment.

2. **Run the Python script**: You can now run the Python script located in the `app` directory. Example for exploring:

```bash
python app/main.py --seed 767 --exploring
```

When you want to run the speed run phase, just remove the `--exploring` flag: