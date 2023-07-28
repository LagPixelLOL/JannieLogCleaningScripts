import os
import json
import re

def main():
    # Prompt user for filename
    filename = input("Enter a filename to save: ")

    # Append .json to the filename
    filename += ".json"

    # Read and merge JSON files in the "jsons" folder
    try:
        merged_data = read_and_merge_json_files("jsons")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Save the resulting JSON array
    try:
        with open(filename, "w", encoding="utf-8") as outfile:
            json.dump(merged_data, outfile, indent=2, ensure_ascii=False)
        print(f"Successfully saved merged data to {filename}.")
    except Exception as e:
        print(f"Error when saving file: {e}")

def read_and_merge_json_files(folder):
    merged_data = []
    file_list = []

    # Iterate through files in the folder and check for .json extension
    for file in os.listdir(folder):
        if file.endswith(".json"):
            file_list.append(file)

    # Remove all the text before "Log_" (including "Log_" itself)
    cleaned_file_mapping = {re.sub(r".*Log_", "", filename): filename for filename in file_list}

    # Sort list in ascending order
    sorted_cleaned_filenames = sorted(cleaned_file_mapping.keys(), key=lambda s: (s.lower(), s))

    # Recreate the sorted list of original filenames
    sorted_original_filenames = [cleaned_file_mapping[cleaned_filename] for cleaned_filename in sorted_cleaned_filenames]

    # Iterate through the sorted files
    for filename in sorted_original_filenames:
        filepath = os.path.join(folder, filename)

        # Load the JSON data and append it to the merged_data list
        try:
            print(f"Processing {filepath} ...")
            with open(filepath, "r", encoding="utf-8") as infile:
                data = json.load(infile)

                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    raise ValueError(f"{filepath} does not contain a JSON array.")
        except Exception as e:
            raise ValueError(f"Error when reading {filepath}: {e}")

    return merged_data

if __name__ == "__main__":
    main()
