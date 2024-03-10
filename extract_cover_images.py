# pip install pymupdf Pillow

import os
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import sys

def extract_cover_pages(pdf_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Iterate through all PDF files in the input directory
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            output_image_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0].replace(" ","_")}.png")
                        # Open the PDF file
            pdf_document = fitz.open(pdf_path)

            # Extract the first page as a pixmap
            first_page = pdf_document[0].get_pixmap()

            # Save the pixmap as a PNG file
            first_page._writeIMG(output_image_path,"jpg","90")
            try:
                # Open the image
                with Image.open(output_image_path) as img:
                    # Resize the image to a 4:3 aspect ratio
                    resized_img = img.resize((300, 400))
                    # resized_img = img.resize((int(img.width * 4/3), img.height))

                    # Save the resized image, overwriting the original file
                    resized_img.save(output_image_path)

            except Exception as e:
                print(f"Error processing '{filename}': {e}")

            # Close the PDF file
            pdf_document.close()
            print(f"![cover](./images/{os.path.basename(output_image_path)})")

if __name__ == "__main__":
    # Replace 'input_directory' and 'output_directory' with your actual paths
    input_directory = sys.argv[1]
    output_directory = os.path.join(input_directory,"images")

    extract_cover_pages(input_directory, output_directory)
