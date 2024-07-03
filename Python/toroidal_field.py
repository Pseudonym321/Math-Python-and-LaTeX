
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
\begin{frame}
\centering
\tdplotsetmaincoords{40}{\Vtheta}
\begin{tikzpicture}[tdplot_main_coords]

%%% DEFINITIONS %%%
\def \Vazi {0}

%%% OUTTER ELLIPSE %%%
%\draw[very thin,tdplot_screen_coords] (0,0,0) circle(1);
%\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
%\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};


%%% FOREACH LOOP %%%
\foreach \Vthe in {0, 10, ..., 350}{
%%% LONGITUTE %%%
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle(1);
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
%%% LATITUTE %%%
\tdplotsetrotatedcoords{\Vazi}{90}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle [radius={cos(\Vthe)}];
\path[tdplot_rotated_coords,draw,very thin,spath/use={pathname, transform={shift={({0},{0},{sin(\Vthe)})}}}];
%%% MAGNETIC FIELD %%%
\foreach \Vdist in {20,40,60}{
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({1/cos(\Vdist)},0,0) circle({sqrt(1/(cos(\Vdist))^2-cos(\Vdist))});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{90}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({-sin(\Vdist)/cos(\Vdist)},0,0) circle({1/cos(\Vdist)});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({sin(\Vdist)/cos(\Vdist)},0,0) circle({1/cos(\Vdist)});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
}

}
\end{tikzpicture}
\end{frame}
\end{document}
'''

def make_tikz_code(angle):
    string = r''
    string += start
    string += r'\newcommand{\Vtheta}{' +f'{angle}' +'}'
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



