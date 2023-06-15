import csv
import os
import random
import re
from unidecode import unidecode

merged_rows = []
already_added_names = []
num_rows = 20 # no. of random rows from top/middle/bottom (bands) to select from
rows_to_add = 5 # rows to add from each band

def sanitize_filename(filename):
    # Define the regex pattern to match the unwanted characters
    #pattern = r'[\/:*?"<>|]'
    filename = unidecode(filename)
    pattern = r'[^a-zA-Z0-9_ ]'

    # Replace the unwanted characters with an empty string
    sanitized_filename = re.sub(pattern, '', filename)

    return sanitized_filename


def merge(new_rows, tag= "None"):
    num_added = 1
    for row in new_rows:
        name = row[0]
        name_sanitized = sanitize_filename(name)
        row[0] = name_sanitized
        chunk_url = row[3]

        if chunk_url == "" or len(name_sanitized) > 50:
            print(f"chunk_url is empty for {name} --->> Skipping !")
            continue
        if len(name_sanitized) > 50:
            print(f"Name too long: {name} --->> Skipping !")
            continue
        
        if name not in already_added_names:
            merged_rows.append(row)
            already_added_names.append(name)
            print(f"{num_added}) {name}\t ({name_sanitized})")
        else:
            print(f"{name} already added!!!!")
            continue

        if "recentlyadded" in tag: # add 25 movies/tv from recently added
            if num_added == 25:
                return
        
        elif "top" in tag: # add 100 movies/tv from top 
            if num_added == 100:
                return
        
        elif num_added == rows_to_add and tag != "all":
            return
        
        elif num_added == rows_to_add*3 and tag == "all":
            return
        
        num_added += 1
        


for file_name in os.listdir("./"):
    if file_name.endswith('.csv') and "500" not in file_name:
        print(file_name)

# Adding Top and recently added movies/tv
directory = './'
file_list = sorted(os.listdir(directory), reverse=True) # sort directory in alphabetical order
for file_name in file_list:
    if file_name.endswith('.csv') and "top" in file_name or "recentlyadded" in file_name and "merged" not in file_name:
        file_path = os.path.join(directory, file_name)
        print("\n\n\n\nfile: ",file_name,"\n\n")
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if present
            
            rows = list(csv_reader)  # Read all rows into a list
            num_total_rows = len(rows)

            merge(rows, file_name)


# Adding remaining
directory = './'
file_list = sorted(os.listdir(directory)) # sort directory in alphabetical order
for file_name in file_list:
    if file_name.endswith('.csv') and "recentlyadded" not in file_name and "top" not in file_name and "merged" not in file_name:
        file_path = os.path.join(directory, file_name)
        print("\n\n\n\n\n\n\n\nfile: ",file_name)
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row if present
            
            rows = list(csv_reader)  # Read all rows into a list
            num_total_rows = len(rows)

            print(f"total rows:{num_total_rows}\trandom_sample={num_rows}\n")
            if num_total_rows <= num_rows*3:
                merge(rows, "all")
                continue

            # Select random rows from the top
            end_index = int(num_total_rows/3)
            print(f"From 0 to {end_index}")
            random_top_rows = random.sample(rows[:end_index], num_rows) # 2 extra in case some are not usable
            merge(random_top_rows)

            # Select random rows from the middle
            start_index = end_index + 1
            end_index = start_index + int(num_total_rows/3)
            print(f"\n\nFrom {start_index} to {end_index}")
            random_middle_rows = random.sample(rows[start_index:end_index], num_rows)
            merge(random_middle_rows)

            # Select random rows from the bottom
            print(f"\n\nFrom {end_index+1} to {num_total_rows-1}")
            random_bottom_rows = random.sample(rows[-num_rows:], num_rows)
            merge(random_bottom_rows)

    #break

output_file = 'merged_urls.csv'
with open(output_file, 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerows(merged_rows)