import sys
from pathlib import Path
import yaml

REQUIRED_FIELDS = {"title", "categories", "author", "date"}
TARGET_FOLDERS = ["Programming Languages", "Scientific Content"]

def validate_front_matter(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if not lines or lines[0].strip() != "---":
        print(f"[ERROR] {file_path}: Missing YAML front matter.")
        return False

    try:
        end_index = lines[1:].index("---\n") + 1
    except ValueError:
        print(f"[ERROR] {file_path}: Unterminated YAML block.")
        return False

    yaml_block = "".join(lines[1:end_index])
    try:
        metadata = yaml.safe_load(yaml_block)
    except yaml.YAMLError as e:
        print(f"[ERROR] {file_path}: Invalid YAML - {e}")
        return False

    if not isinstance(metadata, dict):
        print(f"[ERROR] {file_path}: YAML front matter is not a mapping.")
        return False

    missing = REQUIRED_FIELDS - metadata.keys()
    if missing:
        print(f"[ERROR] {file_path}: Missing fields: {', '.join(missing)}")
        return False

    return True

def main():
    all_valid = True
    for folder in TARGET_FOLDERS:
        folder_path = Path(folder)
        if folder_path.exists() and folder_path.is_dir():
            for file_path in folder_path.rglob("*.qmd"):
                if not validate_front_matter(file_path):
                    all_valid = False
        else:
            print(f"[INFO] Skipping missing folder: {folder}")

    if not all_valid:
        sys.exit("❌ Metadata validation failed.")
    else:
        print("✅ All .qmd files passed metadata validation.")

if __name__ == "__main__":
    main()
