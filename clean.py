import json

remove_if_match_list = [
    "immediate murder", "i.m.p", "sorry, ", " ai ", " ai,", "text based", "text-based", "generate",
    "can't fulfill", "cannot fulfill", "apologize", "apologise", "apologies", "appropriate", "guideline", 
    "ethic", " consen", "ethics", "concern", "well-being", "wellbeing", "instead how about", "moxxie",
    "i cannot do this.", " values", "change topic", "can't engage", "cannot engage", "proxy error"
]

def main():
    input_filename = input("Please enter the file name: ") + ".json"

    try:
        with open(input_filename, "r", encoding="utf-8") as f:
            raw_json = json.load(f)

            if not isinstance(raw_json, list):
                raise ValueError("Invalid JSON format. Expected a JSON array.")

    except FileNotFoundError:
        print(f"Error: File '{input_filename}' not found.")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return

    cleaned_json = []

    for element in raw_json:
        if not (
            isinstance(element, dict)
            and "prompt json" in element
            and "response" in element
        ):
            continue

        response_lower = element["response"].lower()
        if any(remove_str in response_lower for remove_str in remove_if_match_list):
            continue

        try:
            prompt_json = json.loads(element["prompt json"])

            if not isinstance(prompt_json, list):
                raise ValueError("Invalid 'prompt json' format. Expected a JSON array.")

        except ValueError as e:
            print(f"Error: {e}")
            return

        cleaned_prompt_json = []
        skip_element = False

        for prompt in prompt_json:
            if (
                isinstance(prompt, dict)
                and "role" in prompt
                and "content" in prompt
                and prompt["role"] != "system"
            ):
                content_lower = prompt["content"].lower()
                if (content_lower == "just say test"
                    or any(remove_str in content_lower for remove_str in remove_if_match_list)):
                    skip_element = True
                    break
                else:
                    cleaned_prompt_json.append(prompt)

        if not skip_element:
            cleaned_json.append({"prompt": cleaned_prompt_json, "completion": element["response"]})

    output_filename = input("Please enter a filename to save: ") + ".json"

    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(cleaned_json, f, ensure_ascii=False, indent=2)
    except OSError:
        print(f"Error: Failed to save the file '{output_filename}'.")
        return

    print("Operation completed successfully.")

if __name__ == "__main__":
    main()
