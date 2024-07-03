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
%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ANGULAR DEFINITIONS %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def \polar {65}
%\def \azimuth {130}
\def \myscale {1}
%\def \azimuth {0}
\tdplotsetmaincoords{\polar}{\azimuth}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% THE TIKZ ENVIRONMENT %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{tikzpicture}[tdplot_main_coords, scale=\myscale]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% COORDINATE AXES AND GRID %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\draw[-latex] (-4,0,0) -- (4,0,0) node[pos=1,below left]{$x$};
\draw[-latex] (0,-4,0) -- (0,4,0) node[pos=1,below right]{$y$};
\draw[] (-3.75,-3.75) -- (-3.75,3.75) -- (3.75,3.75) -- (3.75,-3.75) -- cycle;
\foreach \x in {-3.75,-3.5,...,3.75}{
\draw[thin,dotted] (\x,-3.75) -- (\x,3.75);}
\foreach \y in {-3.75,-3.5,...,3.75}{
\draw[thin,dotted] (-3.75,\y) -- (3.75,\y);}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% BLANK OUT PARTS ON TOP %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\tdplotsetrotatedcoords{180}{0}{0}
\fill[tdplot_rotated_coords,white] ({cos(\azimuth)},{sin(\azimuth)}) arc [start angle=\azimuth, end angle={\azimuth+180}, radius=1] -- cycle;
\fill[tdplot_screen_coords,white] ({cos(0)},{sin(0)}) arc [start angle=0, end angle=180, radius=1] -- cycle;

%%%%%%%%%%%%%%%%%%%%%%
%%% RIEMANN SPHERE %%%
%%%%%%%%%%%%%%%%%%%%%%

% SCREEN CIRCLE
\draw[tdplot_screen_coords,thin] (1,0) arc [start angle=0, end angle=180,radius=1];
\draw[tdplot_screen_coords,densely dashed,thin] (1,0) arc [start angle=0, end angle=-180,radius=1];

%%% NORTH POLE %%%
\path[tdplot_screen_coords,spath/save=pathname] (0,0) circle [radius=0.045];
\path[fill,spath/use={pathname, transform={shift={(\myscale*0,\myscale*0,\myscale*1)}}}];

%%% XY-PLANE CIRCLE %%%
\tdplotsetrotatedcoords{0}{0}{0}
\draw[tdplot_rotated_coords,densely dashed,thin] (\azimuth:1) arc [start angle=\azimuth, end angle={\azimuth+180}, radius=1];
\draw[tdplot_rotated_coords] (\azimuth:1) arc [start angle=\azimuth, end angle={\azimuth-180}, radius=1];

\path[draw,white,tdplot_screen_coords] (-5.5,-4.5) rectangle (5.5,4.5); 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

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
for i in np.linspace(0+120,30+120,numiter):
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
for i in np.linspace(30+120,0+120,numiter):
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


