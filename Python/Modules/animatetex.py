import subprocess
import shutil
import os
from pypdf import PdfReader, PdfWriter
import subprocess
from reportlab.pdfgen import canvas

def before_loop():
    """
    Purpose:
        Calls file_names() and make_merged() to save space.
    Parameters:
        No parameters.
    Return:
        Void.
    
    """
    file_names()
    make_merged()

def file_names():
    """
    Purpose:
        Declares the names/paths for various temporary files.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    global TeX_file, pdf_file, output_directory, merged_temp, merged_pdf
    TeX_file = "TeX_file.tex"
    pdf_file = "TeX_file.pdf"
    output_directory = r"C:\Users\twill\OneDrive\Documents\Files\Professional\GitHub\Math-Python-and-LaTeX-1"
    merged_temp = 'merged_output_temp.pdf'
    merged_pdf = 'merged_output.pdf'

def make_merged():
    """
    Purpose:
        Makes an initial pdf page, which the gif is appended to - hence remove_first_page()
    Parameters:
        No parameters.
    Return:
        Void.
    """
    global merged_pdf
    merged_pdf = os.path.join(output_directory, merged_pdf)

def during_loop():
    """
    Purpose:
        Calls the functions which compile the tex and append its pdf to the merged pdf.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    compile_tex_to_pdf()
    make_temp()
    append_pdfs(merged_pdf,pdf_file, temp_pdf)
    rename_pdf()


def compile_tex_to_pdf():
    """
    Purpose:
        Function to compile a TeX file to PDF
    Parameters:
        No parameters.
    Return:
        Void.
    """
    subprocess.run(['pdflatex', TeX_file])


def make_temp():
    """
    Purpose:
        Makes a temporary pdf.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    global temp_pdf
    #parent_directory = os.path.dirname(os.path.abspath(__file__))
    parent_directory = output_directory
    temp_pdf = os.path.join(parent_directory, merged_temp)

    c = canvas.Canvas(temp_pdf)
    c.save()

def append_pdfs(pdf1, pdf2, output_pdf):
    """
    Purpose:
        Appends the new pdf to the merged one.
    Parameters:
        pdf1 - initial (big) pdf
        pdf2 - attached pdf
        output_pdf - temp pdf
    Return:
        Void.
    """
    ### FOR CHEAP LAPTOP ###
    #subprocess.run(['gswin64', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    ### FOR FAST LAPTOP ###
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    ### FOR MIKTEX %%%
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])

def rename_pdf():
    """
    Purpose:
        Rename the temporary merged PDF to the original merged PDF
    Parameters:
        No parameters.
    Return:
        Void.
    """
    shutil.move(temp_pdf, merged_pdf)
    #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])

def after_loop():
    """
    Purpose:
        Calls the functions which remove the initial temporary pdf and all those pesky tex files.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
    clean_up()

def remove_first_page(input_pdf, output_pdf):
    """
    Purpose:
        Removes the first page of the merged pdf.
    Parameters:
        input_pdf - the merged pdf
        output_pdf - the final document
    Return:
        Void.
    """
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
        Removes all those pesky tex files.
    Parameters:
        No parameters.
    Return:
        Void.
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
    try:
        os.remove(merged_pdf)
    except FileNotFoundError:
        pass

