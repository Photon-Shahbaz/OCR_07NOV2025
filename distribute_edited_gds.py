import os
import shutil

# Define paths
edited_folder = "edited"
destination_root = r"D:\Edited GDs"

def main():
    for filename in os.listdir(edited_folder):
        if filename.lower().endswith(".png"):
            # Expecting filename format: gd_num gd_date supplier.png
            parts = filename.rsplit(" ", 2)
            if len(parts) != 3:
                print(f"Skipping malformed filename: {filename}")
                continue

            supplier_raw = parts[2].rsplit(".", 1)[0]  # remove .png extension
            supplier_prefix = supplier_raw.strip()[12:]

            # Check if a folder matches the supplier prefix
            found = False
            for folder_name in os.listdir(destination_root):
                if folder_name.upper().startswith(supplier_prefix):
                    source_path = os.path.join(edited_folder, filename)
                    dest_folder = os.path.join(destination_root, folder_name)
                    os.makedirs(dest_folder, exist_ok=True)
                    dest_path = os.path.join(dest_folder, filename)
                    shutil.copy(source_path, dest_path)
                    print(f"✔ Copied '{filename}' to: {dest_folder}")
                    found = True
                    break

            if not found:
                print(f"❌ Supplier folder not found for: {supplier_prefix} (from '{filename}')")

if __name__ == "__main__":
    main()
