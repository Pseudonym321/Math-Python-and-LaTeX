
import numpy as np
from animatetex import *
numiter = 24
preamble= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{pgfplots}
\usepackage{tikz-3dplot}
\pgfplotsset{compat=1.18}
'''
postscript = r'''
\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{60}{110+\Vt}
\begin{tikzpicture}[scale=2,line join=bevel,tdplot_main_coords,%
fill opacity=.5]
\tdplotsetpolarplotrange{0}{360}{0}{360}
\tdplotsphericalsurfaceplot[parametricfill]{72}{36}%
{1+(1/5)*sin(6*\tdplottheta)*sin(5*\tdplotphi)}{black}{\tdplotphi}%
{\path[color=black,thick,->] (0,0,0)
-- (1,0,0) node[anchor=north east]{};}%
{\path[color=black,thick,->] (0,0,0)
-- (0,1,0) node[anchor=north west]{};}%
{\path[color=black,thick,->] (0,0,0)
-- (0,0,1) node[anchor=south]{};}%
\end{tikzpicture}
\end{frame}
\end{document}
'''



output_directory = r''

# Initial PDF file
merged_pdf = os.path.join(output_directory, 'merged_output.pdf') # make this the first frame

for i in np.linspace(0,48,numiter):
    # Create a TeX file for each iteration
    tex_file = 'TeX_file.tex'
    with open(tex_file, 'w') as TeX:
        TeX.write(preamble)
        TeX.write(r'\newcommand{\Vt}{' +f'{i}' +'}')
        TeX.write(postscript)
    compile_tex_to_pdf(tex_file)
    # Append the generated PDF to the merged PDF
    temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
    append_pdfs(merged_pdf, 'file_{}.pdf'.format(1), temp_pdf)

    # Rename the temporary merged PDF to the original merged PDF
    shutil.move(temp_pdf, merged_pdf)
    #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])


remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))

# Clean up - remove individual TeX and PDF files
clean_up()


