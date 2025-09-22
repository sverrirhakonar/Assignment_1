# Assignment_1


# Simple Trading Backtester

This project is a simple tool to test trading ideas. It reads market price data from a file, runs a couple of trading strategies, and shows you how well they performed.

## How to Run
1.  **Set up your environment**. Make sure you have your Python environment (like Anaconda) ready.
2.  **Open the notebook**. Open the `performance.ipynb` file in Jupyter Notebook.
3.  **Run the code**. Run the cells in the notebook from top to bottom.
4.  **See the results**. The notebook will show you the final performance report, including a chart of how the strategies did.

## What's Inside? (File Descriptions)
* **`performance.ipynb`** - The main file. **Run this one to see everything work.**
* **`engine.py`** - The "brain" of the project. It runs the simulation.
* **`strategies.py`** - Contains the different trading ideas (the strategies).
* **`models.py`** - Defines the data structures, like what an "Order" looks like.
* **`data_loader.py`** - A simple tool that reads the `market_data.csv` file.
* **`reporting.py`** - Does the math to calculate the final performance.
* **`market_data.csv`** - The sample price data used for the simulation.