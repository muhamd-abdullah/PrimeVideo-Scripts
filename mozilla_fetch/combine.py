import pandas as pd
import glob


def save_df_to_csv(df, filename):
    df.to_csv(filename, index=False)


def read_csv_files(folder_path):
    # Retrieve CSV file paths from the folder
    #file_paths = glob.glob(folder_path + '/old/*.csv')
    file_paths = glob.glob("./old/*.csv")
    
    dfs = []
    for file_path in file_paths:
        print(file_path)
        # Read CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Remove rows with duplicate values in the "name" column
        df = df.drop_duplicates(subset='name')
        
        # Append the DataFrame to the list
        dfs.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(dfs, ignore_index=True)
    
    return combined_df

# Example usage:
folder_path = '/old'
df = read_csv_files(folder_path)
df = df.drop_duplicates(subset='name')
print(df)
filename = 'output.csv'
save_df_to_csv(df, filename


# Example usage:

)
