import time
import pandas as pd

def compare_csv_files(file1, file2):
    # Read both CSV files into pandas dataframes
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    # Strip leading/trailing spaces from the column names
    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    # ✅ Find common columns
    common_fields = list(set(df1.columns) & set(df2.columns))

    # 🚫 If no common columns found, exit
    if not common_fields:
        print("\n❌ No common fields found between the two files.")
        print("Make sure both CSV files have at least one matching column name.")
        return

    # ✅ Display common fields and let the user choose
    print("\n✅ Common fields found:")
    for i, field in enumerate(common_fields, start=1):
        print(f"{i}. {field}")

    # Select field to merge on
    while True:
        try:
            choice = int(input("\nEnter the number of the field to merge and sort on: ")) - 1
            if 0 <= choice < len(common_fields):
                merge_field = common_fields[choice]
                break
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\n🔗 Merging and sorting on: {merge_field}")

    # ✅ Merge both dataframes on the selected field
    merged = pd.merge(df1, df2, on=merge_field, how='outer', suffixes=('_file1', '_file2'))

    # Fill NaN with 'N/A' for consistent comparison
    merged = merged.fillna("N/A")

    # ✅ Compare the merged DataFrame
    diff = []
    common_columns = [col for col in merged.columns if '_file1' in col]

    for col in common_columns:
        base_col = col.replace('_file1', '')
        col_file1 = f"{base_col}_file1"
        col_file2 = f"{base_col}_file2"

        # Compare values
        column_diff = merged[col_file1] != merged[col_file2]

        if column_diff.any():
            diff.append(f'Column: {base_col}')
            for index, value in column_diff.items():
                if value:
                    diff.append(
                        f"Row {index}: "
                        f"{file1} value: {merged.at[index, col_file1]} vs "
                        f"{file2} value: {merged.at[index, col_file2]}"
                    )

    # ✅ Check for missing or extra rows
    missing_in_file1 = merged[merged[merge_field].isin(df2[merge_field]) & ~merged[merge_field].isin(df1[merge_field])]
    missing_in_file2 = merged[merged[merge_field].isin(df1[merge_field]) & ~merged[merge_field].isin(df2[merge_field])]

    if not missing_in_file1.empty:
        diff.append("\nRows in file2 but missing in file1:")
        diff.append(missing_in_file1.to_string(index=False))

    if not missing_in_file2.empty:
        diff.append("\nRows in file1 but missing in file2:")
        diff.append(missing_in_file2.to_string(index=False))

    # ✅ Print the differences
    if diff:
        for line in diff:
            print("differences found:")
            print(line)
    else:
        print("The data in both files is the same.")
        
    return diff


# ✅ Ask the user for file paths dynamically and handle quotes
print("Hello human O_o ...")
time.sleep(2)
print("i will compare two csv files for you.") 
print("Press ctrl + C to exit at any time.")
print("If your ready to begin please, " )
file1 = input("Enter the full file path for the first CSV file: ").strip().strip('"')
file2 = input("Enter the full file path for the second CSV file: ").strip().strip('"')

# Compare the files
compare_csv_files(file1, file2)

# ✅ Keep the window open using input
input("\nPress Enter to exit...")
