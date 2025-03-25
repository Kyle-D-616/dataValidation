
import pandas as pd

def compare_csv_files(file1, file2):
    # Read both CSV files into pandas DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Strip leading/trailing spaces from the column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # Normalize the DataFrames: sort by columns and rows to avoid ordering issues
    df1 = df1.sort_values(by=list(df1.columns)).reset_index(drop=True)
    df2 = df2.sort_values(by=list(df2.columns)).reset_index(drop=True)

    # Check if the data is the same
    if df1.equals(df2):
        print("The data in both files is the same.")
        return True
    else:
        print("The data is not the same, here is the difference:")
        for column in df1.columns:
            diff = df1[column] != df2[column]
            diffRows= df1[diff]

        return False
    print(f"Differing rows for column '{column}':")
    print(diffRows)

# Example usage
file1 = 'testfile1.csv'
file2 = 'testfile2.csv'
compare_csv_files(file1, file2)
