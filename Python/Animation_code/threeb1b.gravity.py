
import numpy as np
import os
import shutil
numiter = 24
start = r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts}
\usepackage{tikz,scalerel,pict2e}
\usepackage{tikz-3dplot,tkz-euclide}
\usepackage{comment}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}


\begin{document}
\begin{frame}
'''
end = r'''
\begin{tikzpicture}[scale=0.3]
\path[name path=circle,draw] (0,0) circle [radius=5cm];
\path[fill] (3,0) circle [radius=0.2]; %replace with nodes?
\path[fill] (0,0) circle [radius=0.2];

\foreach \i in {1,2,...,24}
{
  \edef\optname{name path global=line\i}
  \expandafter\path\expandafter[\optname] (3,0) -- ++(15*\i:10);
  \path[name intersections={of=circle and line\i}] (intersection-1);
  \path[spath/save=name](3,0) -- (intersection-1);
  \path[draw,spath/use={name,transform={rotate around={\p:(spath cs:name .5)}}}=\name];
};
\draw[white] (-6,-6) rectangle (6,6);
\end{tikzpicture}
\end{frame}
\end{document}
'''

def make_tikz_code(angle):
    string = r''
    string += start
    string += r'\newcommand{\p}{' +f'{angle}' +'}'
    string += end
    return string



from pypdf import PdfReader, PdfWriter

def remove_first_page(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Add all pages except the first one
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)


import subprocess

output_directory = r''

# Function to compile a TeX file to PDF
def compile_tex_to_pdf(tex_file):
    subprocess.run(['pdflatex', tex_file])

# Function to append two PDF files
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])


# Initial PDF file
merged_pdf = os.path.join(output_directory, 'merged_output.pdf') # make this the first frame



for i in np.linspace(0,90,numiter//2):
    # Create a TeX file for each iteration
    tex_file = 'file_{}.tex'.format(1)
    string = make_tikz_code(i)
    with open(tex_file, 'w') as f:
        f.write(string)
    
    # Compile the TeX file to PDF
    compile_tex_to_pdf(tex_file)

    # Append the generated PDF to the merged PDF
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, 'file_{}.pdf'.format(1), temp_pdf)

    # Rename the temporary merged PDF to the original merged PDF
    shutil.move(temp_pdf, merged_pdf)
    #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])

for i in np.linspace(90,0,numiter//2):
    # Create a TeX file for each iteration
    tex_file = 'file_{}.tex'.format(1)
    string = make_tikz_code(i)
    with open(tex_file, 'w') as f:
        f.write(string)

    # Compile the TeX file to PDF
    compile_tex_to_pdf(tex_file)

    # Append the generated PDF to the merged PDF
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, 'file_{}.pdf'.format(1), temp_pdf)

    # Rename the temporary merged PDF to the original merged PDF
    shutil.move(temp_pdf, merged_pdf)
    #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])




remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
