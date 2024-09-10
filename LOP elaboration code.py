import pandas as pd
import os
import glob

# MEAN AND STD CALCULATION PART
# Load the CSV file
file_path = "C:/Users/jacop/OneDrive - Wageningen University & Research/General/3D scans/MTG data analysis/LOP data analysis/LOP_Data_DAT27.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Identifying the columns from which to calculate mean and standard deviation
columns_to_calculate = data.columns[14:]

# Grouping the data by 'plant_density', 'leaf_side' and 'LOP_key'
grouped_data = data.groupby(['plant_density', 'leaf_side', 'LOP_key'])

# Calculating mean and standard deviation
mean_df = grouped_data[columns_to_calculate].mean().reset_index()
std_df = grouped_data[columns_to_calculate].std().reset_index()

# Renaming columns to indicate mean and standard deviation
mean_df.columns = [str(col) + '_mean' if col in columns_to_calculate else col for col in mean_df.columns]
std_df.columns = [str(col) + '_std' if col in columns_to_calculate else col for col in std_df.columns]

# Merging mean and std dataframes
merged_df = pd.merge(mean_df, std_df, on=['plant_density', 'leaf_side', 'LOP_key'])

# Saving the final dataframe to a new CSV file
output_file_path = "C:/Users/jacop/OneDrive - Wageningen University & Research/General/3D scans/MTG data analysis/LOP data analysis/LOP_Data_DAT27_mean_std.csv"
merged_df.to_csv(output_file_path, index=False)


# COMBINATION OF VALUES INTO STRINGS
# Function to concatenate column values into a single string
def concatenate_columns(data, column_pattern):
    return data.filter(like=column_pattern).apply(lambda x: ';'.join(x.astype(str)), axis=1)

# Load the CSV file
file_path = "C:/Users/jacop/OneDrive - Wageningen University & Research/General/3D scans/MTG data analysis/LOP data analysis/LOP_Data_DAT27_mean_std.csv"
data = pd.read_csv(file_path)

# Process each unique combination of 'plant_density', 'upper_side', and 'LOP_key'
output_files = []
for (plant_density, leaf_side, lop_key), group in data.groupby(['plant_density', 'leaf_side', 'LOP_key']):
    # Concatenate mean and std values
    group['combined_mean'] = concatenate_columns(group, '_mean')
    group['combined_std'] = concatenate_columns(group, '_std')
    
    # Define new column names based on upper_side and LOP_key
    new_mean_col_name = f"{leaf_side}_{lop_key}_mean"
    new_std_col_name = f"{leaf_side}_{lop_key}_std"
    
    # Rename the combined columns
    group.rename(columns={'combined_mean': new_mean_col_name, 'combined_std': new_std_col_name}, inplace=True)

    # Select only necessary columns
    final_columns = ['plant_density', 'leaf_side', 'LOP_key', new_mean_col_name, new_std_col_name]
    final_group = group[final_columns]

    # Save to CSV
    output_filename = f"C:/Users/jacop/OneDrive - Wageningen University & Research/General/3D scans/MTG data analysis/LOP data analysis/filtered_LOP_data/filtered_LOP_data_{plant_density}_{leaf_side}_{lop_key}.csv"  
    final_group.to_csv(output_filename, index=False)
    output_files.append(output_filename)


# Folder where your subset files are stored
input_folder = "C:/Users/jacop/OneDrive - Wageningen University & Research/General/3D scans/MTG data analysis/LOP data analysis/filtered_LOP_data/"

# Pattern to match all subset files
file_pattern = os.path.join(input_folder, "*.csv")

# List to hold all DataFrames
all_dataframes = []

# Iterate over each file and append to list
for file in glob.glob(file_pattern):
    df = pd.read_csv(file)
    
    # Drop the 'leaf_side' and 'LOP_key' columns if they exist in the dataframe
    df = df.drop(columns=['leaf_side', 'LOP_key'], errors='ignore')

    all_dataframes.append(df)

# Check if any DataFrames were added to the list
if not all_dataframes:
    print("No files were found or read. Please check the file pattern and directory.")
else:
    # Concatenate all dataframes
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # Save the combined DataFrame to a new CSV file
    output_file = os.path.join(input_folder, "combined_LOP_data.csv")
    combined_df.to_csv(output_file, index=False)

    print(f"Combined file saved as: {output_file}")