import os

def delete_gd(folder_path):
    # List all files in the specified folder
    for file_name in os.listdir(folder_path):
        # Check if the file name starts with "GD-" and has a .pdf extension
        if file_name.startswith("GD-") and file_name.endswith(".png"):
            # Construct the full file path
            file_path = os.path.join(folder_path, file_name)

            try:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")


# Specify the folder path
folder_path = r"C:\Users\HP\PycharmProjects\Image_processing-master\images\static"

# Run the deletion function
delete_gd(folder_path)
