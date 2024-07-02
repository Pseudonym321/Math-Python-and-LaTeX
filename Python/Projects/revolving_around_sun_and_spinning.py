
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
\newcommand{\Vazi}{0}
\newcommand{\Vpol}{30}
"""
postscript = r"""

\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords,scale=0.5]
%%% AXES %%%
%\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
%\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};

\foreach \Vthe in {0, 10, ..., 170}{
%%% MAIN SPHERE %%%
\tdplotsetrotatedcoords{0}{0}{0}
%%% LONGITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({1.5*cos(\t)*cos(\Vthe)},{1.5*cos(\t)*sin(\Vthe)},{1.5*sin(\t)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
%%% LATITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({1.5*cos(\t)*sin(\Vthe)},{1.5*sin(\t)*sin(\Vthe)},{1.5*cos(\Vthe)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];}

%%% OUTER ORBIT %%%
\draw[dashed,very thin] (0,0) circle(6);

%%% SPHERE 1 %%%
\tdplotsetrotatedcoords{\Vazi}{\Vpol}{0}
%%% OUTER CIRCLE 1 %%%
\path[tdplot_screen_coords,spath/save=pathname] ({0},{0},0) circle(1);
\draw[very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];
%%% AXIS OF ROTATION 1 %%%
\path[tdplot_rotated_coords,spath/save=pathname] ({0},{0},-3.5) -- (0,0,4);
\draw[very thin,-latex,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];
%%% ARC OF ROTATION 1 %%%
\path[tdplot_rotated_coords,spath/save=pathname,very thin,domain=0:270,smooth,variable=\t] plot ({0.3*cos(\t)},{0.3*sin(\t)},{2.75});
\draw[very thin,-latex,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];
%%% LONGITUDE AND LATITUDE %%%
\foreach \Vthe in {0, 20, ..., 160}{
%%% LONGITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({cos(\t)*cos(\Vthe+\Vspin)},{cos(\t)*sin(\Vthe+\Vspin)},{sin(\t)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];
%%% LATITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({cos(\t)*sin(\Vthe)},{sin(\t)*sin(\Vthe)},{cos(\Vthe)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];}

%%% INNER ORBIT %%%
\path[dashed,spath/save=pathname] ({0},{0},0) circle(3);
\path[draw,black,very thin,dashed,spath/use={pathname, transform={shift={({3*cos(\Vang)},{3*sin(\Vang)},{0})}}}];

%%% OUTER CIRCLE 2 %%%
\path[tdplot_screen_coords,spath/save=pathname] ({0},{0},0) circle(0.45);
\path[draw,black,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)+1.5*cos(\Vangle)},{3*sin(\Vang)+1.5*sin(\Vangle)},{0})}}}];

%%% SPHERE 2 %%%
\tdplotsetrotatedcoords{\Vazi}{-\Vpol}{0}
%%% AXIS OF ROTATION 1 %%%
\path[tdplot_rotated_coords,spath/save=pathname] ({0},{0},-1) -- (0,0,1.5);
\path[draw,black,-latex,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)+1.5*cos(\Vangle)},{3*sin(\Vang)+1.5*sin(\Vangle)},{0})}}}];
%%% ARC OF ROTATION 1 %%%
\path[tdplot_rotated_coords,spath/save=pathname,very thin,domain=0:270,smooth,variable=\t] plot ({0.3*cos(\t)},{0.3*sin(\t)},{0.75});
\path[draw,black,-latex,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)+1.5*cos(\Vangle)},{3*sin(\Vang)+1.5*sin(\Vangle)},{0})}}}];
%%% LONGITUDE AND LATITUDE %%%
\foreach \Vthe in {0, 20, ..., 160}{
%%% LONGITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({0.45*cos(\t)*cos(\Vthe+\Vspin)},{0.45*cos(\t)*sin(\Vthe+\Vspin)},{0.45*sin(\t)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)+1.5*cos(\Vangle)},{3*sin(\Vang)+1.5*sin(\Vangle)},{0})}}}];
%%% LATITUDE %%%
\path[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t,spath/save=pathname] plot ({0.45*cos(\t)*sin(\Vthe)},{0.45*sin(\t)*sin(\Vthe)},{0.45*cos(\Vthe)});
\path[draw,black,very thin,spath/use={pathname, transform={shift={({3*cos(\Vang)+1.5*cos(\Vangle)},{3*sin(\Vang)+1.5*sin(\Vangle)},{0})}}}];}


\draw[white,tdplot_screen_coords] (0,0) circle(10);

\end{tikzpicture}
\end{frame}
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
for angle in range(0,360,360//24):
    with open(tex_file, "w") as tex:
        tex.write(preamble)
        new_line = f"\\newcommand{{\\Vspin}}{{{angle*2}}}\n"
        tex.write(new_line)
        new_line = f"\\newcommand{{\\Vang}}{{{angle}}}\n"
        tex.write(new_line)
        new_line = f"\\newcommand{{\\Vangle}}{{{angle*2}}}\n"
        tex.write(new_line)
        tex.write(postscript)
    compile_tex_to_pdf(tex_file)
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, pdf_file, temp_pdf)
    shutil.move(temp_pdf, merged_pdf)
remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))
