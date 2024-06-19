import Riemann_integral as Ri
import subprocess, shutil
import os
from pypdf import PdfReader, PdfWriter
preamble = r"""\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
\begin{document}
\begin{frame}
\centering
\begin{tikzpicture}[scale=3]
\draw[thick,-latex] (-1.3,0) -- (1.3,0);
\draw[thick,-latex] (0,-0.3) -- (0,2.3);
\draw[domain=-1.23:1.18,smooth,variable=\Vt]
  plot (\Vt,{\Vt*\Vt*\Vt-0.5*\Vt+1},0);
\draw[] (-1,0) -- (-1,2) node[pos=1,above]{$a$};
\draw[] (1,0) -- (1,2) node[pos=1,above]{$b$};
"""
postscript = r"""\end{tikzpicture}
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

merged_pdf = os.path.join("", 'merged_output.pdf')



for num in range (5,27):
    with open("TeX_file.tex", "w") as tex:
        tex.write(preamble)
        delta, inputs = Ri.Riemann_sum(-1,1,num)
        for input in inputs:
            new_line = f"\\draw[] ({input},0) -- ({input},{{{input}^3-0.5*{input}+1}}) -- ++({delta},0) |- (0,0);\n"
            tex.write(new_line)
        tex.write(postscript)
    subprocess.run(['pdflatex', r'TeX_file.tex'])
    temp_pdf = os.path.join("TeX_file.pdf", 'merged_output_temp.pdf')
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + "TeX_file.pdf", os.path.abspath(merged_pdf), os.path.abspath(temp_pdf)])
    shutil.move(temp_pdf, merged_pdf)
remove_first_page(merged_pdf, os.path.join(merged_pdf, 'final_output.pdf'))
    