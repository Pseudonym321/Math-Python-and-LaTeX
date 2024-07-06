
import numpy as np
import Modules.animatetex as animatetex

numiter = 24

preamble= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''

postscript = r'''
\begin{document}
\centering
\tdplotsetmaincoords{0}{90}
\begin{tikzpicture}[tdplot_main_coords]
\draw[white,tdplot_main_coords] (-4.5,-3.5) rectangle (4.5,5);
\tdplotsetrotatedcoords{0}{0}{0}
\draw[tdplot_rotated_coords,domain=90:\Vn,smooth,very thin,samples=5000,variable=\Vt] plot ({sqrt(1-(\Vt/360)^2)*sin(40*\Vt)/(1-sqrt(1-(\Vt/360)^2)*cos(40*\Vt)))},{(\Vt/360)/(1-sqrt(1-(\Vt/360)^2)*cos(40*\Vt))*cos(3*\Vt)},{(\Vt/360)/(1-sqrt(1-(\Vt/360)^2)*cos(40*\Vt))*sin(3*\Vt)});
\end{tikzpicture}
\end{document}
'''

def main():
    """
    Purpose:
        Makes a spinning loxodrome projection.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    animatetex.before_loop()
    for n in np.linspace(90,360,numiter):
        with open(animatetex.TeX_file, 'w') as TeX:
            TeX.write(preamble)
            TeX.write(r'\newcommand{\Vn}{' +f'{n}' +'}')
            TeX.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()