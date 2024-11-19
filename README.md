# MTG and LOP Data Processing and Statistical Analysis

## Repository Overview

This repository contains Python scripts designed to process and analyze data related to plant architecture from MTG and LOP datasets. Each script serves a specific purpose, from preprocessing and statistical analysis to generating visual outputs.

## Files

### 1. `MTG elaboration final.py`

This script processes and organizes MTG (Multiscale Tree Graph) data through several steps:
- **Division into Subfiles**: Splits data into internode and leaf-specific CSV files based on unique dates and densities.
- **Statistical Calculations**: Computes mean and standard deviation for specific columns.
- **Representative MTG Generation**: Combines and reorders data for analysis while maintaining specified column orders.
- **Data Sorting**: Applies custom sorting for `order1` and `order2` categories and recalculates mean anticlockwise rotation for specific leaf orders.

#### Key Functionalities:
- Dynamic folder creation for organized data storage.
- Conversion of specific units (e.g., mm to m).
- Custom sorting based on plant architecture.
- Outputs processed and sorted data files.

#### Outputs:
- Subdivided CSV files organized by date, density, and plant order.
- Representative MTG files with mean and standard deviation values.
- Final sorted data ready for visualization or further analysis.

---

### 2. `LOP elaboration code.py`

This script focuses on preprocessing and statistical analysis of LOP (Leaf Optical Properties) data.

#### Key Functionalities:
- **Mean and Standard Deviation Calculation**: Groups data by `plant_density`, `leaf_side`, and `LOP_key` to compute statistics for relevant columns.
- **String Combination**: Concatenates calculated values into formatted strings for easier representation.
- **Data Combination**: Merges multiple processed CSV files into a consolidated dataset.

#### Outputs:
- CSV files containing grouped statistical data for different LOP keys.
- Combined CSV summarizing all processed LOP data.

---

### 3. `MTG_statistics_architecture.py`

This script performs statistical analyses on MTG data to explore variations across plant architectures.

#### Key Functionalities:
- **ANOVA and Variance Analysis**: Evaluates differences across plant densities and architectural elements.
- **Normality Testing**: Uses Shapiro-Wilk tests for normality checks within groups.
- **Boxplot Generation**: Visualizes data distributions for selected metrics.

#### Outputs:
- Statistical result files for ANOVA, variance, and normality tests.
- Boxplots saved as images to visualize distribution and variability.

---

## Usage

### Setup
1. Install required dependencies:
    ```bash
    pip install pandas numpy matplotlib scipy
    ```
2. Ensure all data files are available in the specified directories.

### Execution
Run each script in your preferred Python environment, ensuring that the paths to input files and directories are correctly set.

### Customization
Modify column names, excluded columns, or desired statistical tests as needed in each script to adapt to your specific dataset requirements.

---

## Outputs

All processed data and generated statistics are saved in respective directories:
- **`internode_data/`**: Contains processed internode-specific data.
- **`leaf_data/`**: Contains processed leaf-specific data.
- **`mean_sd_leaf_internode_data/`**: Mean and standard deviation files for selected columns.
- **`representative_MTG/`**: Combined and representative MTG files.
- **`sorted_representative_MTG/`**: Sorted MTG data for visualization.
- **`output_statistics_architecture/`**: Statistical results and boxplots for MTG analysis.
- **`filtered_LOP_data/`**: Grouped and processed LOP files.
- **`combined_LOP_data.csv`**: Consolidated dataset summarizing all LOP data.

