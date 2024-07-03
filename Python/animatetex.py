
import subprocess
import shutil
import os
from pypdf import PdfReader, PdfWriter
import subprocess

def file_names():
    global TeX_file, pdf_file
    TeX_file = "TeX_file.tex"
    pdf_file = "TeX_file.pdf"

def make_merged():
    global output_directory, merged_pdf
    output_directory = r''
    merged_pdf = os.path.join(output_directory, 'merged_output.pdf')


# Function to compile a TeX file to PDF
def compile_tex_to_pdf(tex_file):
    """
    Purpose:
    
    
    """
    subprocess.run(['pdflatex', tex_file])

def make_temp():
    global temp_pdf
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')


# Function to append two PDF files
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])

def rename_pdf():
    """
    Purpose:
        Rename the temporary merged PDF to the original merged PDF
    
    """
    shutil.move(temp_pdf, merged_pdf)
    #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])

def remove_first_page(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Add all pages except the first one
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

def clean_up():
    """
    Purpose:
    Parameters:
    Return:
    """
    try:
        os.remove('TeX_file.tex')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.pdf')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.aux')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.log')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.nav')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.out')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.snm')
    except FileNotFoundError:
        pass
    try:
        os.remove('TeX_file.toc')
    except FileNotFoundError:
        pass

