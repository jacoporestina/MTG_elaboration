import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import f_oneway, levene, shapiro

def analyze_mtg_data(file_path, output_folder, excluded_columns):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    data = pd.read_csv(file_path)

    # Print all column names in the dataset
    print("All columns in the dataset:", data.columns.tolist())

    for date in data['Date'].unique():
        date_data = data[data['Date'] == date]

        for order_type in ['order1', 'order2']:
            order_data = date_data[~date_data[order_type].isna()]
            date_order_folder = os.path.join(output_folder, f"{date}_{order_type}")
            if not os.path.exists(date_order_folder):
                os.makedirs(date_order_folder)

            columns_to_analyze = [col for col in order_data.columns[6:] if col not in excluded_columns]

            # Print columns that are being analyzed
            print(f"Analyzing the following columns for {order_type} on {date}: {columns_to_analyze}")

            for column in columns_to_analyze:
                if order_data[column].isna().all():
                    continue

                results_file_path = os.path.join(date_order_folder, f'statistics_{column}.txt')
                with open(results_file_path, 'w') as results_file:
                    for element in order_data[order_type].unique():
                        element_data = order_data[order_data[order_type] == element]
                        unique_densities = element_data['Density'].unique()
                        groups = [element_data[element_data['Density'] == density][column].dropna() for density in unique_densities]
                        valid_groups = [group for group in groups if len(group) >= 3]

                        if len(valid_groups) >= 2:
                            # ANOVA
                            f_value, p_value = f_oneway(*valid_groups)
                            results_file.write(f"ANOVA results for {element} {column}:\nF-value: {f_value}, P-value: {p_value}\n")

                            # Levene's Test for Equal Variances
                            variance_p_value = levene(*valid_groups)[1]
                            results_file.write(f"Levene's Test for Equal Variances p-value: {variance_p_value}\n")

                            # Normality test
                            normality_results = {density: shapiro(group)[1] for density, group in zip(unique_densities, groups) if len(group) >= 3}
                            results_file.write("Normality test p-values by density:\n")
                            for density, p_val in normality_results.items():
                                results_file.write(f"{density}: {p_val}\n")

                        # Boxplot
                        for column in columns_to_analyze:
                            try:
                                plt.figure(figsize=(10, 6))

                                elements = order_data[order_type].unique()
                                densities = order_data['Density'].unique()
                                plot_data = []
                                plot_labels = []

                                for element in elements:
                                    for density in densities:
                                        element_density_data = order_data[
                                            (order_data[order_type] == element) & (order_data['Density'] == density)][
                                            column]
                                        plot_data.append(element_density_data)
                                        plot_labels.append(f"{element}_{density}")

                                positions = np.arange(1, len(plot_data) * 2, 2)
                                plt.boxplot(plot_data, positions=positions)

                                plt.xticks(positions, plot_labels, rotation=45)
                                plt.ylabel(column)
                                plt.title(f'Boxplot of {column} for all elements in {order_type} on {date}')
                                plt.savefig(
                                    os.path.join(date_order_folder, f'boxplot_{order_type}_{column}.png'))
                                plt.close()
                            except ValueError as e:
                                print(f"Error creating boxplot for {column} in {order_type} on {date}: {e}")


file_path = "MTG.csv"
output_folder = "output_statistics_architecture"
excluded_columns = ['phyllotaxis segments leaf (°)', 'Length segments leaf (mm)', 'Inclination segments leaf (°)',
                    'Phyllotaxis 1st leaf segment (°)', 'Phyllotaxis 2nd leaf segment (°)', 'Phyllotaxis 3rd leaf segment (°)', 'Phyllotaxis 4th leaf segment (°)',
                    'Length 1st segment (mm)', 'Length 2nd segment (mm)', 'Length 3rd segment (mm)', 'Length 4th segment (mm)',
                    'Inclination 1st leaf segment (°)', 'Inclination 2nd leaf segment (°)', 'Inclination 3rd leaf segment (°)', 'Inclination 4th leaf segment (°)', ]

analyze_mtg_data(file_path, output_folder, excluded_columns)
