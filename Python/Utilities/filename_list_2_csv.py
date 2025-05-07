import os
import csv
from tkinter import Tk, filedialog

# Variables for file paths
directory_path = None
output_csv_path = None

def directory_filenames_to_csv(directory_path, output_csv_path):
    try:
        # Get list of filenames in the directory
        filenames = os.listdir(directory_path)
        
        # Write filenames (without extensions) to a CSV file
        with open(output_csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Filename"])  # Header row
            for filename in filenames:
                name_without_extension = os.path.splitext(filename)[0]
                writer.writerow([name_without_extension])
        
        print(f"Filenames from '{directory_path}' have been written to '{output_csv_path}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Hide the root Tkinter window
    Tk().withdraw()
    
    # Let the user select the folder containing the files
    directory_path = filedialog.askdirectory(title="Select Folder with Files")
    if not directory_path:
        print("No folder selected. Exiting.")
        exit()
    
    # Let the user select the output CSV file location and name
    output_csv_path = filedialog.asksaveasfilename(
        title="easements_test",
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")]
    )
    if not output_csv_path:
        print("No file selected. Exiting.")
        exit()
    
    # Call the function
    directory_filenames_to_csv(directory_path, output_csv_path)