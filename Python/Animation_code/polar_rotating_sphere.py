
import subprocess
import shutil
import os
from pypdf import PdfReader, PdfWriter
preamble = r"""
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%%% PACKAGES %%%
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
%%% DEFINITIONS %%%
\newcommand{\Vazi}{120}
"""
postscript = r"""
\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{50}{120}
\begin{tikzpicture}[tdplot_main_coords]
%%% OUTTER ELLIPSE %%%
\draw[very thin,tdplot_screen_coords] (0,0,0) circle(1);
\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};
%%% FOREACH LOOP %%%
\foreach \Vthe in {0, 10, ..., 350}{
%%% LONGITUTE %%%
\tdplotsetrotatedcoords{\Vthe+\Vazi}{90}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle(1);
\path[draw,black,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
%%% LATITUTE %%%
\tdplotsetrotatedcoords{\Vazi}{\Vpol}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle [radius={cos(\Vthe)}];
\path[tdplot_rotated_coords,draw,blue,very thin,spath/use={pathname, transform={shift={({0},{0},{sin(\Vthe)})}}}];
}
\end{tikzpicture}
\end{frame}
\end{document}"""



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
for angle in range(0,360,360//24):
    with open(tex_file, "w") as tex:
        tex.write(preamble)
        new_line = f"\\newcommand{{\\Vpol}}{{{angle}}}\n"
        tex.write(new_line)
        tex.write(postscript)
    compile_tex_to_pdf(tex_file)
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, pdf_file, temp_pdf)
    shutil.move(temp_pdf, merged_pdf)
remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
