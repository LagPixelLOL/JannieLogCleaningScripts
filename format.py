import json
import os

def main():
    input_filename = input("Enter the input filename: ") + ".json"

    if not os.path.exists(input_filename):
        print(f"Error: File {input_filename} not found.")
        return

    try:
        with open(input_filename, "r", encoding="utf-8") as input_file:
            data = json.load(input_file)
    except Exception as e:
        print(f"Error: Could not read file {input_filename}. {e}")
        return

    formatted_list = []

    if isinstance(data, list):
        for obj in data:
            if not (isinstance(obj, dict) and "prompt" in obj and "completion" in obj):
                continue

            formatted = ""
            prompts = obj["prompt"]

            if isinstance(prompts, list):
                for prompt_item in prompts:
                    if not (isinstance(prompt_item, dict) and "role" in prompt_item and "content" in prompt_item):
                        continue

                    content = prompt_item["content"]
                    role = prompt_item["role"]

                    if isinstance(content, str):
                        if role == "assistant":
                            formatted += "\n### Output: "
                        else:
                            formatted += "\n### Input: "
                        formatted += content.strip()

            completion = obj["completion"]

            formatted_dict = {
                "input": formatted.strip() + "\n### Output:",
                "output": completion.strip()
            } if isinstance(completion, str) else None

            if formatted_dict:
                formatted_list.append(formatted_dict)

    output_filename = input("Enter the output filename: ") + ".json"

    try:
        with open(output_filename, "w", encoding="utf-8") as output_file:
            json.dump(formatted_list, output_file, indent=2, ensure_ascii=False)
        print(f"File {output_filename} saved successfully!")
    except Exception as e:
        print(f"Error: Could not save file {output_filename}. {e}")

if __name__ == "__main__":
    main()
