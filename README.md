# SDX-Transformer

The sdx-transformer service provides data transformation functionality for SDX. 
It is used to transform both survey submission data into pck files on the journey downstream, and for transforming the data headed upstream for pre-population.

## Getting Started

### 1. Install Poetry:
   - This project uses Poetry for dependency management. Ensure Poetry is installed on your system.
   - If you have poetry installed, you can skip this step.
   - If Poetry is not installed, you can install it using:
```bash
brew install poetry
```
or
```bash
brew install pipx
pipx install poetry
```
- Use the official Poetry installation guide for other installation methods: https://python-poetry.org/docs/#installation
- Verify the installation by using the following command:
```bash
poetry --version
```

### 2. Install Dependencies:
   - Install the project dependencies using Poetry by running the following command at the project root:
```bash
poetry install
```
This will create a new virtual environment if one does not already exist and install the dependencies into it.

### 3. Run the tests:
   - To run all the tests, use the following command or use the Makefile:
```bash
poetry run pytest -v --cov-report term-missing --disable-warnings --cov=app tests/
```

### 4. Run the transformer:
   - To run the transformer, use the following command:
```bash
poetry run python run.py
```
