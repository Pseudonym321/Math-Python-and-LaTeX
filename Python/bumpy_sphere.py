
import numpy as np
import animatetex
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

def main():
    """
    
    
    
    """
    animatetex.before_loop()
    for theta in np.linspace(0,48,numiter):
        with open(animatetex.TeX_file, 'w') as TeX:
            TeX.write(preamble)
            TeX.write(r'\newcommand{\Vt}{' +f'{theta}' +'}')
            TeX.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()


