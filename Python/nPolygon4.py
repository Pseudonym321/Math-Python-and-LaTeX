
import subprocess
import shutil
import os
from pypdf import PdfReader, PdfWriter
preamble = r"""
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
"""
postscript = r"""
\begin{document}
\centering
\begin{tikzpicture}[scale=2]
\foreach \Vs in {0}{
\foreach \Vt in {1,2,...,\Vnmo}{
%%% ORIGINAL VECTORS %%%
\draw[-latex] ({cos(90+(\Vs*360/\Vn))},{sin(90+(\Vs*360/\Vn))}) -- ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))});
%%% FRAME %%%
\draw[] ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))}) -- ({cos(90+((\Vt+1)*360/\Vn))},{sin(90+((\Vt+1)*360/\Vn))});}}

\draw[white] (-2,-2) rectangle (2,2);
\end{tikzpicture}
\end{document}
"""



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
for angle in range(3,12,1):
    with open(tex_file, "w") as tex:
        tex.write(preamble)
        new_line = r"\def \Vn {" + f"{angle}" + "}\n"
        tex.write(new_line)
        new_line = r"\def \Vnmo {" + f"{angle-1}" + "}\n"
        tex.write(new_line)
        tex.write(postscript)
    compile_tex_to_pdf(tex_file)
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, pdf_file, temp_pdf)
    shutil.move(temp_pdf, merged_pdf)
remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
