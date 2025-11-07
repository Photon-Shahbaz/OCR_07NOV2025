import os
from PIL import Image
import pytesseract
import shutil
from delete_files import delete_gd

# Optional: specify Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

def extract_text_and_crop(image_path, x, y, width, height):
    try:
        img = Image.open(image_path)
        bbox = (x, y, x + width, y + height)
        cropped_img = img.crop(bbox)
        extracted_text = pytesseract.image_to_string(cropped_img)
        return extracted_text.strip(), cropped_img
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return "", None

def sanitize_filename(name):
    """Remove or replace characters not allowed in filenames."""
    return "".join(c if c.isalnum() or c in " _-()" else "_" for c in name)

def process_image_file(image_file, input_folder, output_folder, edited_folder):
    image_path = os.path.join(input_folder, image_file)

    regions = {
        "supplier": (94, 229, 640, 40),
        "gd_num":   (93, 2605, 223, 72)
    }

    results = {}

    for label, (x, y, w, h) in regions.items():
        text, cropped_img = extract_text_and_crop(image_path, x, y, w, h)
        if cropped_img:
            output_img_name = f"{os.path.splitext(image_file)[0]}_{label}.png"
            output_img_path = os.path.join(output_folder, output_img_name)
            cropped_img.save(output_img_path)
            print(f"{label} cropped image saved to: {output_img_path}")
        results[label] = text
        print(f"{label} extracted text: {text}")

    # Assign variables
    supplier = results.get("supplier", "").strip()
    raw_gd_text = results.get("gd_num", "").replace("\n", "").strip()
    gd_date = raw_gd_text[-10:] if len(raw_gd_text) >= 10 else ""
    gd_num = raw_gd_text[5:14] if len(raw_gd_text) >= 14 else ""

    print("\n--- Final Variables ---")
    print(f"Supplier: {supplier}")
    print(f"GD Number: {gd_num}")
    print(f"GD Date: {gd_date}")

    results["gd_num"] = gd_num
    results["gd_date"] = gd_date

    # Save extracted text to a file
    text_output_path = os.path.join(output_folder, os.path.splitext(image_file)[0] + "_text.txt")
    with open(text_output_path, "w", encoding="utf-8") as f:
        for key, value in results.items():
            f.write(f"{key}: {value}\n")
    print(f"Extracted text saved to: {text_output_path}")

    # Rename and move file
    new_filename = f"{sanitize_filename(gd_num)} {sanitize_filename(gd_date)} {sanitize_filename(supplier)}.png"
    new_image_path = os.path.join(edited_folder, new_filename)

    try:
        shutil.copy(image_path, new_image_path)
        print(f"Renamed input file saved to: {new_image_path}\n")
    except Exception as e:
        print(f"Error saving renamed file: {e}")

def main():
    input_folder = r"C:\Users\HP\PycharmProjects\Image_processing-master\images\static"
    output_folder = "output"
    edited_folder = "edited"
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(edited_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().startswith("gd-") and filename.lower().endswith((".png", ".jpg", ".jpeg")):
            print(f"\n=== Processing File: {filename} ===")
            process_image_file(filename, input_folder, output_folder, edited_folder)



if __name__ == "__main__":
    main()
