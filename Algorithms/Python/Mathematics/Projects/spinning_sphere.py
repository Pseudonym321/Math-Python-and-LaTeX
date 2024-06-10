# %%
import numpy as np
import os
import shutil
from PyPDF2 import PdfReader, PdfWriter
import subprocess

# %%
numiter = 30

# %%
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts}
\usepackage{tikz}
\usepackage{scalerel,pict2e,tkz-euclide,tikz-3dplot}
\usetikzlibrary{patterns,arrows.meta,calc,shadows,external}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\usetikzlibrary{perspective,spath3}
\usepackage{comment}
\begin{document}
'''

# %%
end = r'''
\begin{frame}
\centering
\def \myscale {1}
\tdplotsetmaincoords{65}{\azimuth}
\begin{tikzpicture}[tdplot_main_coords,scale=\myscale]
\draw[tdplot_screen_coords] (0,0) circle [radius=1];
\foreach \t in {0, 10, ..., 350}{
\begin{scope}
%\clip[] (-2,-2,0) rectangle (2,2,2);
\tdplotsetrotatedcoords{90}{\t}{0}
\draw[tdplot_rotated_coords,very thin] (0,0) circle [radius=1];
\tdplotsetrotatedcoords{180}{90}{0}
\draw[tdplot_rotated_coords,very thin] (0,0,{sin(\t)}) circle [radius={cos(\t)}];
\end{scope}}
\clip[tdplot_screen_coords] (-5,-3) rectangle (5,3);
\draw[tdplot_screen_coords,white] (-4.9,-2.9) rectangle (4.9,2.9); 
\foreach \k in {10,20,...,80}{
%%% on C %%%
\draw[] ({1/cos(\k)},0) circle [radius={sqrt(1/(cos(\k)^2)-cos(\k))}];
\draw[] (0,{-sin(\k)/cos(\k)}) circle [radius={1/cos(\k)}];
}
\foreach \k in {100,110,...,170}{
%%% on C %%%
\draw[] ({1/cos(\k)},0) circle [radius={sqrt(1/(abs(cos(\k))^2)-abs(cos(\k)))}];
\draw[] (0,{-sin(\k)/cos(\k)}) circle [radius={1/cos(\k)}];
}
\draw[] (0,0) circle [radius=1];
\draw[] (0,-7,0) -- (0,7,0); % circle at infinity
\draw[] (-7,0,0) -- (7,0,0); % circle at infinity

%%% axes %%%
\draw[-latex,thick] (-2,0,0) -- (2,0,0) node[pos=1,below left]{$x,\xi$}; % x-axis
\draw[-latex,thick] (0,-3.5,0) -- (0,3.5,0) node[pos=1,below right]{$y,\eta$}; % y-axis
\draw[-latex,thick] (0,0,-2) -- (0,0,1.5) node[pos=1,above right]{$z,\zeta$}; % z-axis
\end{tikzpicture}
\end{frame}

\end{document}

'''

# %%
def make_tikz_code(angle):
    tikz_code = r''
    tikz_code += start
    tikz_code += r'\def \azimuth {' + f'{angle}' + '}'
    tikz_code += end
    return tikz_code

# %%
def remove_first_page(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Add all pages except the first one
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)

# %%
output_directory = r''

# %%
# Function to compile a TeX file to PDF
def compile_tex_to_pdf(tex_file):
    subprocess.run(['pdflatex', tex_file])

# %%
# Function to append two PDF files
gs_path = r"C:\Program Files\gs\gs10.03.1\bin\gswin64c.exe"
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run([gs_path, '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])

# %%
# Initial PDF file
merged_pdf = os.path.join(output_directory, 'merged_output.pdf') # make this the first frame

# %%
for i in np.linspace(120,150,numiter):
    # Create a TeX file for each iteration
    tex_file = 'file_{}.tex'.format(1)
    tikz_code = make_tikz_code(i)
    with open(tex_file, 'w') as f:
        f.write(tikz_code)

    # Compile the TeX file to PDF
    compile_tex_to_pdf(tex_file)

    # Append the generated PDF to the merged PDF
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, 'file_{}.pdf'.format(1), temp_pdf)

    # Rename the temporary merged PDF to the original merged PDF
    shutil.move(temp_pdf, merged_pdf)

for i in np.linspace(150,120,numiter):
    # Create a TeX file for each iteration
    tex_file = 'file_{}.tex'.format(1)
    tikz_code = make_tikz_code(i)
    with open(tex_file, 'w') as f:
        f.write(tikz_code)

    # Compile the TeX file to PDF
    compile_tex_to_pdf(tex_file)

    # Append the generated PDF to the merged PDF
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, 'file_{}.pdf'.format(1), temp_pdf)

    # Rename the temporary merged PDF to the original merged PDF
    shutil.move(temp_pdf, merged_pdf)


# %%
print('Merged PDF file:', merged_pdf)

# %%
remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))

# %%
# Clean up - remove individual TeX and PDF files
try:
    os.remove('file_1.tex')
except FileNotFoundError:
    pass  # Ignore if the file is not found
try:
    os.remove('file_1.pdf')
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
try:
    pass
    os.remove('merged_output.pdf')
except FileNotFoundError:
    pass  # Ignore if the file is not found
print('Cleaned up temporary files.')


