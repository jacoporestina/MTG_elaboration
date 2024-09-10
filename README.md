# MTG Data Analysis Pipeline

This repository contains Python scripts to process and analyze MTG (Modular Tree Growth) data from 3D scans. The pipeline performs the following tasks:

1. **MTG Division in Sub Files**: Splits the main dataset into smaller CSV files based on dates, densities, and orders.
2. **Mean and Standard Deviation Calculation**: Computes mean and standard deviation for specified columns in the divided files.
3. **Representative MTG Generation**: Combines and adjusts the mean and standard deviation data into representative MTG files.
4. **Sorting Data**: Sorts the representative MTG files based on a custom-defined order.

## Dependencies

- Python 3.x
- pandas
- os
- glob

Install the required dependencies with:
```bash
pip install pandas
```

## Usage

1. Place `MTG.csv` in the appropriate directory.
2. Run each script in sequence to process the data.
3. Check the output folders for results.

## Output Files

- **`internode_data/` and `leaf_data/`**: Divided data files.
- **`mean_stdev_leaf_internode_data/`**: Files with calculated statistics.
- **`Representative_MTG/`**: Combined representative MTG files.
- **`Sorted_MTG_Data/`**: Sorted MTG data files.
