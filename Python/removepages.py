import fitz

# Path of the input PDF file
input_file = r"C:\Users\twill\OneDrive\Documents\GitHub\My Algorithms\final_output.pdf"
# Path for the output PDF file
output_file = r"modified_test.pdf"

# Opening the PDF file and creating a handle for it
file_handle = fitz.open(input_file)
for i in range(60):
    # The page number to be deleted (indexing starts from 0)
    page = 0

    # Deleting the specified page
    file_handle.delete_page(page)

    # Saving the modified PDF file
    file_handle.save(output_file)
