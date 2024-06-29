
import numpy as np
import os
import shutil
numiter = 24
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''
end = r'''
\begin{document}
\tdplotsetmaincoords{45}{\Vt}
\begin{tikzpicture}[tdplot_main_coords,scale=0.75]
%%% AXES %%%

\draw[-latex] (0,0,0) -- (5,0,0) node[pos=1]{$x$};
\draw[-latex] (0,0,0) -- (0,5,0) node[pos=1]{$y$};
\draw[-latex] (0,0,0) -- (0,0,5) node[pos=1]{$z$};

\coordinate (A) at (1,-1,-1);
\coordinate (B) at (-1,1,-1);
\coordinate (C) at (-1,-1,1);
\coordinate (D) at (1,1,1);

%%% BLUE %%%
\draw[fill,opacity=0.3,blue] (A) -- (B) -- (D) -- cycle;
\draw[fill,opacity=0.3,red] (B) -- (D) -- (C) -- cycle;
\draw[fill,opacity=0.3,green] (D) -- (C) -- (A) -- cycle;
\draw[fill,opacity=0.3,black] (A) -- (B) -- (C) -- cycle;

%%% POINTS %%%
\path[tdplot_screen_coords,spath/save=point] (0,0,0) circle(0.1);
%%% INITIAL %%%
%\fill[blue][spath/use={point, transform={shift={({1},{2},{1})}}}]; %a

\draw[white,tdplot_screen_coords] (-6,-6) rectangle (6,6);
\end{tikzpicture}
\end{document}
'''

def make_tikz_code(angle):
    string = r''
    string += start
    string += r'\newcommand{\Vt}{' +f'{angle}' +'}\n'
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

for i in np.linspace(0,360,numiter):
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



