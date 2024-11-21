import argparse
from pdf2image import convert_from_path

# Function to generate an image from the first page of a PDF
def generate_first_page_image(pdf_path):
    # Convert the first page of the PDF to an image
    images = convert_from_path(pdf_path, first_page=1, last_page=1, size=400)
    
    # Save the first page as an image
    image_path = f'{pdf_path}_first_page.png'
    images[0].save(image_path, 'PNG')

    print(f"First page of '{pdf_path}' has been saved as: {image_path}")

# Main function to parse arguments and call the image generation function
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate an image of the first page of a PDF.")
    
    # Add argument for the input PDF file
    parser.add_argument('pdf_path', type=str, help="Path to the input PDF file")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Call function to generate the first page image
    generate_first_page_image(args.pdf_path)

if __name__ == "__main__":
    main()

