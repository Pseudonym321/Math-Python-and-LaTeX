
import numpy as np
import os
import shutil
numiter = 24
start = r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%maths
\usepackage{mathtools,amsmath,amssymb,amsfonts,physics}
\usepackage{tikz,scalerel,pict2e,ifthen}
\usepackage{tikz-3dplot,tkz-euclide}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\def \p {1.75}
\def \q {4}
\begin{document}
\begin{frame}

'''

end = r'''

\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords,scale=0.7]
\coordinate (O) at (0,0);
\coordinate (V1) at (0:\p);
\coordinate (V2) at (\t:\q);
\path[draw,white] (-5,-5) -- (5,5);

\draw[] (\p,0) arc [start angle=360, end angle=180, radius=\p] -- (\p,0) -- cycle;
\draw[dotted] (-\p,0) arc [start angle=180, end angle=0, radius=\p];

\draw[] (0,0) -- (270:\q) arc [start angle=270, end angle=\t, radius=\q];

%%% VECTORS %%%
\draw[-Triangle] (0,0) -- (V2) node[pos=1,above] {$\va{q}$};
\draw[-Triangle] (0,0) -- (V1) node[pos=1,right] {$\va{p}$};

%%% GEOMETRY %%%
\fill[red,opacity=0.2] (0,0) -- ++(\t:\p) -- ++(0,-\q) -- ++(\t+180:\p);
\draw[] (0,0) -- ++(\t:\p) -- ++(0,-\q) -- ++(\t+180:\p) -- cycle;

\fill[blue,opacity=0.2] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q);
\draw[] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q) -- cycle;
\draw[blue,-Triangle] (0,0,0) -- (0,0,{\p*\q*sin(\t)}) node[left]{$\va{p}\cross\va{q}$};
\draw[white,tdplot_screen_coords] (-5,-6) rectangle (5,6);
\end{tikzpicture}


\end{frame}

\end{document}
'''

end2 = r"""
\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords,scale=0.7]
\coordinate (O) at (0,0);
\coordinate (V1) at (0:\p);
\coordinate (V2) at (\t:\q);
\path[draw,white] (-5,-5) -- (5,5);

\draw[] (\p,0) arc [start angle=0, end angle=180, radius=\p] -- (\p,0) -- cycle;
\draw[dotted] (-\p,0) arc [start angle=180, end angle=360, radius=\p];

\draw[] (0,0) -- (90:\q) arc [start angle=90, end angle=\t, radius=\q];

%%% VECTORS %%%
\draw[-Triangle] (0,0) -- (V2) node[pos=1,above] {$\va{q}$};
\draw[-Triangle] (0,0) -- (V1) node[pos=1,right] {$\va{p}$};

%%% GEOMETRY %%%
\fill[red,opacity=0.2] (0,0) -- ++(\t:\p) -- ++(0,\q) -- ++(\t+180:\p);
\draw[] (0,0) -- ++(\t:\p) -- ++(0,\q) -- ++(\t+180:\p) -- cycle;

\fill[blue,opacity=0.2] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q);
\draw[] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q) -- cycle;
\draw[blue,-Triangle] (0,0,0) -- (0,0,{\p*\q*sin(\t)}) node[left]{$\va{p}\cross\va{q}$};
\draw[white,tdplot_screen_coords] (-5,-6) rectangle (5,6);

\end{tikzpicture}


\end{frame}

\end{document}
"""

def make_tikz_code(angle):
    string = r''
    string += start
    string += r'\def \t {' + f'{angle}' + r'}'
    if angle <= 180:  
        string += end2
    else:
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
