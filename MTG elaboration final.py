import pandas as pd
import os
import glob


# MTG DIVISION IN SUB FILES PART

# Create directories if they do not exist
os.makedirs("internode_data", exist_ok=True)
os.makedirs("leaf_data", exist_ok=True)
os.makedirs("mean_sd_leaf_internode_data", exist_ok=True)
os.makedirs("representative_MTG/", exist_ok=True)
os.makedirs("sorted_representative_MTG", exist_ok=True)

# Specify the CSV file and variables to analyze
csv_file = "MTG_csv.csv"

# Read the data from the CSV file
data = pd.read_csv(csv_file)

# Iterate through all dates
for date in data['date'].unique():
    # Filter data for the current date
    filtered_data = data.loc[data['date'] == date]

    # Iterate through all densities
    for density in filtered_data['density'].unique():
        # Filter data for the current density
        density_data = filtered_data.loc[filtered_data['density'] == density]

        # Iterate through each element of Order 1
        for order in density_data["order1"].unique():
            if pd.notna(order):  # Check for NaN before processing
                internode_data = density_data.loc[density_data['order1'] == order]
                print(internode_data)
                internode_file_path = f"internode_data/internode_data{order}_{date}_{density}.csv"
                internode_data.to_csv(internode_file_path, index=False)

        # Iterate through each element of Order 2
        for order in density_data["order2"].unique():
            if pd.notna(order):  # Check for NaN before processing
                leaf_data = density_data.loc[density_data['order2'] == order]
                print(leaf_data)
                leaf_file_path = f"leaf_data/leaf_data{order}_{date}_{density}.csv"
                leaf_data.to_csv(leaf_file_path, index=False)

# MEAN AND STD CALCULATION PART

def calculate_stats(data, columns):
    mean_values = data[columns].mean()
    std_values = data[columns].std()
    return mean_values, std_values

def process_data(input_folder, output_folder, columns_to_calculate, all_columns, keep_columns, columns_to_convert):
    for csv_file in glob.glob(os.path.join(input_folder, "*.csv")):
        data = pd.read_csv(csv_file).convert_dtypes()
        
        # Create copies of the columns_to_calculate and all_columns lists
        columns_to_calculate_copy = columns_to_calculate.copy()
        all_columns_copy = all_columns.copy()

        # Convert specified columns from mm to meters and rename
        for col in columns_to_convert:
            if col in data.columns:
                data[col] = data[col] / 1000  # Convert from mm to meters
                new_col_name = f"{col[:-4]}(m)"  # Change '_(mm)' to '_(m)'
                data.rename(columns={col: new_col_name}, inplace=True)
                columns_to_calculate_copy = [new_col_name if x == col else x for x in columns_to_calculate_copy]
                all_columns_copy = [new_col_name if x == col else x for x in all_columns_copy]

        # Now that we have renamed the columns, ensure to work with the updated lists
        try:
            filtered_data = data[keep_columns + columns_to_calculate_copy].copy()

            mean_values, std_values = calculate_stats(filtered_data, columns_to_calculate_copy)

            for col, mean_val, std_val in zip(columns_to_calculate_copy, mean_values, std_values):
                filtered_data.loc[:, f'mean_{col}'] = [mean_val] * len(filtered_data)
                filtered_data.loc[:, f'sd_{col}'] = [std_val] * len(filtered_data)

            # Select keep columns, mean, and sd columns
            result_data = filtered_data[keep_columns +
                                        [f'mean_{col}' for col in columns_to_calculate_copy] +
                                        [f'sd_{col}' for col in columns_to_calculate_copy]].iloc[:1].copy()

            result_data.to_csv(os.path.join(output_folder, f"mean_sd_{os.path.basename(csv_file)}"), index=False)
            print(os.path.basename(csv_file))

        except (ValueError, KeyError, ZeroDivisionError) as e:
            print(f"{os.path.basename(csv_file)} - Error calculating mean and sd: {str(e)}")


# Specify folders and columns for internode and leaf data
internode_data_folder = "internode_data/"
leaf_data_folder = "leaf_data/"
output_folder = "mean_sd_leaf_internode_data/"

all_columns = ['length_(mm)', 'phyllotaxis_relative_(°)', 'inclination_(°)', 
                             'width_(mm)', 'total_length_segments_(mm)', 'length_petiolule_(mm)', 
                             'inclination_petiolule_(°)', 'total_leaf_area_(m2)']

keep_columns = ["date", "density", "order1", "order2", "order", "rank", "probability_%", 
                "upper_transmittance", "upper_reflectance", "lower_transmittance", "lower_reflectance", 
                'quantum_efficiency', 'Amax', 'convexity'] 

columns_to_convert = {'length_(mm)', 'width_(mm)', 'length_petiolule_(mm)', 'total_length_segments_(mm)'}  # Define the columns to be converted from mm to m

columns_to_calculate = all_columns  # This assumes you want to calculate stats for all these columns

# Process internode data
process_data(internode_data_folder, output_folder, all_columns, columns_to_calculate, keep_columns, columns_to_convert)

# Process leaf data
process_data(leaf_data_folder, output_folder, all_columns, columns_to_calculate, keep_columns, columns_to_convert)

print("mean and sd calculation completed")


# REPRESENTATIVE MTG GENERATION PART

def combine_and_adjust_csv_files(input_directory, output_directory, desired_column_order):
    all_files = os.listdir(input_directory)
    files_dict = {}

    for file_name in all_files:
        if file_name.endswith('.csv'):
            file_path = os.path.join(input_directory, file_name)
            df = pd.read_csv(file_path)
            key = (df['date'].iloc[0], df['density'].iloc[0])
            files_dict.setdefault(key, []).append(df)

    for key, dfs in files_dict.items():
        combined_df = pd.concat(dfs, ignore_index=True)

        # Ensure column names in desired_column_order are present in combined_df
        valid_columns = [col for col in desired_column_order if col in combined_df.columns]
        missing_columns = [col for col in desired_column_order if col not in combined_df.columns]
        if missing_columns:
            print(f"Warning: The following columns were listed in desired_column_order but are missing in the DataFrame: {missing_columns}")

        # Append remaining columns not in desired_column_order at the end
        remaining_columns = [col for col in combined_df.columns if col not in valid_columns]
        final_column_order = valid_columns + remaining_columns

        combined_df = combined_df[final_column_order]

        # Save the combined and reordered DataFrame
        output_file_name = f"representative_MTG_{key[0]}_{key[1]}.csv"
        output_file_path = os.path.join(output_directory, output_file_name)
        combined_df.to_csv(output_file_path, index=False)
        print(f"Combined file {output_file_name} has been saved.")

# Files directory
input_folder = "mean_sd_leaf_internode_data/"
output_folder = "representative_MTG/"

# Define your desired column order
desired_column_order = [
    "date", "density", "order1", "order2", "order", "rank", "probability_%", 
    'mean_phyllotaxis_relative_(°)', 'sd_phyllotaxis_relative_(°)', 
    'mean_inclination_(°)', 'sd_inclination_(°)',
    'mean_length_(m)', 'sd_length_(m)', 
    'mean_width_(m)', 'sd_width_(m)', 
    'mean_total_leaf_area_(m2)', 'sd_total_leaf_area_(m2)',
    'mean_length_petiolule_(m)', 'sd_length_petiolule_(m)',
    'mean_total_length_segments_(m)', 'sd_total_length_segments_(m)',
    'mean_inclination_petiolule_(°)', 'sd_inclination_petiolule_(°)',
    'quantum_efficiency', 'Amax', 'convexity',
    'upper_reflectance', 'upper_transmittance',  
    'lower_reflectance', 'lower_transmittance', 
    
]
                        
# Call the function
combine_and_adjust_csv_files(input_folder, output_folder, desired_column_order)


# SORTING DATA PART

# Folder path containing your CSV files
input_folder_path = "representative_MTG/"

# Specify the new folder path
output_folder_path = "sorted_representative_MTG/"

# Create the new folder if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Read each CSV file separately, sort, and save to the new folder
for filename in os.listdir(input_folder_path):
    if filename.endswith(".csv"):
        # Read the CSV file
        file_path = os.path.join(input_folder_path, filename)
        df = pd.read_csv(file_path)

        # Define a custom sorting order for 'order1' and 'order2'
        custom_sort_order = {'I0': 0, 'I1': 1, 'xL1': 2, 'xL2': 3, 'I2': 4, 'xL3': 5, 'I3': 6, 'xL4': 7, 'I4': 8, 'xL5': 9, 'I5': 10, 'xL6': 11, 'I6': 12, 'xL7': 13, 'I7': 14, 'xL8': 15, 'I8': 16, 'xL9': 17, 'I9': 18, 'xL10': 19, 'I10': 20, 'xL11': 21, 'I11': 22, 'xL12': 23}

        # Create a temporary column to store the sorting order
        df['sorting_order'] = df.apply(lambda row: custom_sort_order.get(row['order1']) if not pd.isna(row['order1']) else custom_sort_order.get(row['order2']), axis=1)

        # Sort the DataFrame based on the 'sorting_order' column
        df = df.sort_values(by=['sorting_order'])

        # Drop the temporary column used for sorting
        df = df.drop(columns=['sorting_order'])

        # Reset index after sorting
        df = df.reset_index(drop=True)

        # Calculate mean_anticlockwise_rotation only for 'order2' values with xL1, xL2, etc.
        df['mean_anticlockwise_rotation_(°)'] = 0.0  # Initialize the new column
        cumulative_rotation = 0  # Starting point

        for i, row in df.iterrows():
            order2_value = str(row['order2'])  # Get the value in 'order2'
            if 'xL' in order2_value:  # Only process rows with xL1, xL2, etc.
                if order2_value == 'xL1':
                    df.at[i, 'mean_anticlockwise_rotation_(°)'] = 0  # Set xL1 to 0
                    cumulative_rotation = 0  # Reset for new sequence
                else:
                    # Add the previous leaf's phyllotaxis relative to the cumulative sum
                    cumulative_rotation += df.at[i, 'mean_phyllotaxis_relative_(°)']
                    df.at[i, 'mean_anticlockwise_rotation_(°)'] = cumulative_rotation
        
        # Replace mean_phyllotaxis_relative with mean_anticlockwise_rotation
        df['mean_phyllotaxis_relative_(°)'] = df['mean_anticlockwise_rotation_(°)']

        # Drop the 'mean_anticlockwise_rotation_(°)' column as it's no longer needed
        df = df.drop(columns=['mean_anticlockwise_rotation_(°)'])

        # Save the sorted DataFrame to a new CSV file in the new folder
        output_file_path = os.path.join(output_folder_path, f"sorted_{filename}")
        df.to_csv(output_file_path, index=False)

        print(f"Sorted data saved to: {output_file_path}")











