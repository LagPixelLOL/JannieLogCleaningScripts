import json
import os

def main():
    input_filename = input("Enter JSON filename: ") + ".json"
    if not os.path.isfile(input_filename):
        print(f"Error: File '{input_filename}' does not exist.")
        return
    
    try:
        with open(input_filename, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            if not isinstance(data, list):
                print("Error: JSON content must be an array.")
                return
    except json.JSONDecodeError:
        print(f"Error: '{input_filename}' is not a valid JSON file.")
        return

    output_filename = input("Enter filename to save: ") + ".jsonl"
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            for item in data:
                json.dump(item, outfile, ensure_ascii=False)
                outfile.write('\n')
        print(f"Successfully converted '{input_filename}' to JSONL format in '{output_filename}'.")
    except Exception as e:
        print(f"Error: Could not save file '{output_filename}'. Reason: {e}")

if __name__ == '__main__':
    main()
