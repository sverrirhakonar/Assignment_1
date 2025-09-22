# Simple Trading Backtester

This project is a simple tool to test trading ideas. It reads market price data from a file, runs a couple of trading strategies, and shows you how well they performed.

## How to Run
1.  **Set up your environment**. Make sure you have your Python environment (like Anaconda) ready.
2.  **Open the notebook**. Open the `Performance_Comparison.ipynb` file in Jupyter Notebook.
3.  **Run the code**. Run the cells in the notebook from top to bottom.
4.  **See the results**. The notebook will show you the final performance report, including charts comparing the strategies.

## What's Inside? (File Descriptions)
* **`Performance_Comparison.ipynb`** - The main notebook. **Run this to see the full analysis and charts.**
* **`main.py`** - A simple script to run the simulation from the command line.
* **`engine.py`** - The "brain" of the project. It runs the simulation.
* **`strategies.py`** - Contains the different trading ideas (the strategies).
* **`models.py`** - Defines the data structures, like what an "Order" looks like.
* **`data_loader.py`** - A simple tool that reads the `market_data.csv` file.
* **`data_generator.py`** - Creates the `market_data.csv` file with fake price data.
* **`reporting.py`** - Does the math to calculate the final performance.
* **`unit_tests.py`** - Contains tests to make sure individual parts of the code work correctly.
* **`market_data.csv`** - The sample price data used for the simulation.
* **`performance.md`** - A simple report file generated from the notebook, easy to view on GitHub.