
import numpy as np
import os
import shutil
numiter = 24*5
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''
end = r'''
\newcommand{\Pa}{0}
\newcommand{\Pb}{0}
\newcommand{\Pc}{0}
\newcommand{\Ua}{(-2)}
\newcommand{\Ub}{2}
\newcommand{\Uc}{1}
\newcommand{\Vr}{1.5}
\newcommand{\Va}{(\Vr*sin(4*\Vt)*(1-(\Vt/360)^2)^(0.5))}
\newcommand{\Vb}{(\Vr*(\Vt/360))}
\newcommand{\Vc}{(\Vr*cos(4*\Vt)*(1-(\Vt/360)^2)^(0.5))}
\begin{document}
\centering
\tdplotsetmaincoords{45}{120}
\begin{tikzpicture}[tdplot_main_coords,scale=0.75]
%%% AXES %%%
%\draw[-latex] (0,0,0) -- (5,0,0) node[pos=1]{$x$};
%\draw[-latex] (0,0,0) -- (0,5,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,0) -- (0,0,5) node[pos=1]{$z$};

%%% POINTS %%%
\path[tdplot_screen_coords,spath/save=point] (0,0,0) circle(0.1);
%\fill[][spath/use={point, transform={shift={({-1},{0},{1})}}}];

%%% COORDINATES %%%
\coordinate (O) at (0,0,0);
\coordinate (P) at ({\Pa},{\Pb},{\Pc});
\coordinate (U) at ({\Pa+\Ua},{\Pb+\Ub},{\Pc+\Uc});
\coordinate (V) at ({\Pa+(\Va)},{\Pb+(\Vb)},{\Pc+(\Vc)});
\coordinate (UandV) at ({\Pa+(\Ua+\Va)},{\Pb+\Ub+\Vb},{\Pc+\Uc+\Vc});
\coordinate (CP) at ({\Pa+(\Ub*\Vc-\Uc*\Vb)},{\Pb-(\Ua*\Vc-\Uc*\Va)},{\Pc+(\Ua*\Vb-\Ub*\Va)});



\draw[domain=-360:360,very thin,smooth,samples=500,variable=\t]
  plot ({\Pa+\Vr*sin(4*\t)*(1-(\t/360)^2)^(0.5)},{\Pb+\Vr*\t/360},{\Pc+\Vr*cos(4*\t)*(1-(\t/360)^2)^0.5});


%%% VECTOR V %%%
\draw[thick,-latex] (O) -- ({\Va},{\Vb},{\Vc});

%%% VECTOR U %%%
\draw[thick,-latex] (O) -- ({\Ua},{\Ub},{\Uc});

%%% BLUE AREA %%%
\fill[blue,opacity=0.3] (O) -- (U) -- (UandV) -- (V);

%%% BLUE VECTOR %%%
\draw[blue,-latex,thick] (O) -- (CP);

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

for i in np.linspace(-360,360,numiter):
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



