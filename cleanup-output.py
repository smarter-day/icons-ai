import json

def clean_icons(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Process each icon and remove specified fields
    for icon in data.get("icons", []):
        icon.pop("style", None)
        icon.pop("width", None)
        icon.pop("height", None)
        icon.pop("content", None)
        icon.pop("set_id", None)

        if "categories" in icon:
            for category in icon["categories"]:
                icon["categories"][category] = []

    # Write the cleaned data to the output file
    with open(output_file + ".json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    with open(output_file + ".compressed.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)

# Input and output file paths
input_file = "data/filtered_icons_3276.json"  # Replace with your input file path
output_file = "data/filtered_icons_3276.clean"  # Replace with your output file path

clean_icons(input_file, output_file)
