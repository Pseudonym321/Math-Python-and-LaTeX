
import subprocess
import shutil
import os
from pypdf import PdfReader, PdfWriter
def latex(n):
    LaTeX = r"""
    \documentclass{beamer}
    \beamertemplatenavigationsymbolsempty
    \usepackage{tikz}
    """

    LaTeX += r"""
    \begin{document}
    \centering
    \begin{tikzpicture}[scale=2.5]
    """

    big_draw = r"\foreach \Vt in {0,1,...," + f"{n}" +"}{\n"
    for i in range(1,n+1):
        big_draw += r"\draw[-latex] (0,0) -- ({cos(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))},{sin(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))});" +"\n"
        big_draw += r"\draw[] ({cos(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))},{sin(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))}) -- ({cos(90+((" + f"{i}" + r"+1)*360/" + f"{n}" + r"))},{sin(90+((" + f"{i}" + r"+1)*360/" + f"{n}" + r"))});}"
    LaTeX += big_draw

    big_draw = r"""
    \draw[] (0,0) -- ({cos(90)},{sin(90)})
    """
    for i in range(1,n+1):
        big_draw += r" -- ++({cos(90+((" + f"{i}" + r")*360/" + f"{n}" + r"))},{sin(90+((" + f"{i}" + r")*360/" + f"{n}" + r"))})" +"\n"
    big_draw += ";\n"

    LaTeX += big_draw



    LaTeX += r"""
    \draw[white] (-1.5,-1.5) rectangle (1.5,1.5);
    \end{tikzpicture}
    \end{document}
    """

    return LaTeX


def remove_first_page(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Add all pages except the first one
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)


# Function to compile a TeX file to PDF
def compile_tex_to_pdf(tex_file):
    subprocess.run(['pdflatex', tex_file])

# Function to append two PDF files
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])

tex_file = "TeX_file.tex"
pdf_file = "TeX_file.pdf"
output_directory = r''
merged_pdf = os.path.join(output_directory, 'merged_output.pdf')
for angle in range(2,10,1):
    with open(tex_file, "w") as tex:
        tex.write(latex(angle))
    compile_tex_to_pdf(tex_file)
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, pdf_file, temp_pdf)
    shutil.move(temp_pdf, merged_pdf)
remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
