
import numpy as np
import os
import shutil
numiter = 20
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%maths
\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{autobreak}
\usepackage{comment}
%tikzpicture
\usepackage{tikz}
\usepackage{scalerel}
\usepackage{pict2e}
\usepackage{tkz-euclide}
\usepackage{tikz-3dplot}
\usetikzlibrary{calc}
\usetikzlibrary{patterns,arrows.meta}
\usetikzlibrary{shadows}
\usetikzlibrary{external}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\usetikzlibrary{perspective,spath3}

'''
end = r'''


\newcommand{\myscale}{2.1}
\begin{document}
\begin{frame}
\begin{tikzpicture}[scale=\myscale]
%%% GEOMETRY %%%
\draw[] (0,0) circle [radius=1];
\draw[] (0,0) -- (\mytheta:1);

%%% LINES %%%
\draw[] (0,1) -- ({cos(\mytheta)},{sin(\mytheta)});
\draw[] (0,1) -- ({cos(\mytheta)/(1-sin(\mytheta))},0);

\fill[] ({cos(\mytheta)/(1-sin(\mytheta))},0) circle [radius=0.05];
\draw[] ({cos(\mytheta)},{sin(\mytheta)}) -- ({cos(\mytheta)},{-sin(\mytheta)});
\fill[] ({cos(\mytheta)},{-sin(\mytheta)}) circle [radius=0.05];

\draw[] (0,1) -- ({cos(\mytheta)},{-sin(\mytheta)});
\draw[] (0,1) -- ({cos(\mytheta)/(1+sin(\mytheta))},0);
\fill[] ({cos(\mytheta)/(1+sin(\mytheta))},0) circle [radius=0.05];

\draw[thin,densely dotted] ({cos(\mytheta)/(1-sin(\mytheta))},0) -- ({cos(\mytheta)/(1-sin(\mytheta))},-1.3);
\draw[thin,densely dotted] ({cos(\mytheta)/(1+sin(\mytheta))},0) -- ({cos(\mytheta)/(1+sin(\mytheta))},-1.3);
\draw[|-|] ({cos(\mytheta)/(1-sin(\mytheta))},-1.3) -- ({cos(\mytheta)/(1+sin(\mytheta))},-1.3);



%%% AXES %%%
\draw[-latex,thick] (0,0) -- (0,2);
\draw[-latex,thick] (-1.5,0) -- (3,0);

%%% NODES %%%
\fill[] (0,0) circle [radius=0.05];
\fill[] (0,1) circle [radius=0.05];
%\fill[] (\mytheta+180:1) circle [radius=0.05];
\fill[] (\mytheta:1) circle [radius=0.05];
\draw[red,|-Latex] ({1/cos(\mytheta)},-1.5) -- ({1/cos(\mytheta)},0);
\end{tikzpicture}
\end{frame}
\end{document}
'''

def make_tikz_code(angle):
    string = r''
    string += start
    string += r'\newcommand{\mytheta}{' +f'{angle}' +'}'
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
gs_path = r"C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe"
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run([gs_path, '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])


# Initial PDF file
merged_pdf = os.path.join(output_directory, 'merged_output.pdf') # make this the first frame

for i in np.linspace(0,50,numiter):
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

for i in np.linspace(50,0,numiter):
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

# Clean up - remove individual TeX and PDF files
for i in np.linspace(-30,50,numiter):
    try:
        os.remove('file_{}.tex'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.pdf'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.aux'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.log'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.nav'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.out'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.snm'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.toc'.format(1))
    except FileNotFoundError:
        pass  # Ignore if the file is not found



print('Cleaned up temporary files.')
print('Merged PDF file:', merged_pdf)



