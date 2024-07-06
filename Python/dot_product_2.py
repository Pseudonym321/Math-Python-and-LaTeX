
import numpy as np
import Modules.animatetex as animatetex

numiter = 24

start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%maths
\usepackage{mathtools,amsmath,amssymb,amsfonts,physics}
\usepackage{tikz,scalerel,pict2e}
\usepackage{tikz-3dplot,tkz-euclide}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\begin{document}
\begin{frame}
'''

end = r'''
\begin{tikzpicture}[scale=1]
\draw[white] (-2,-2) rectangle (2,7);
\coordinate (O) at (0,0);
\coordinate (V1) at (0:1.75);
\coordinate (V2) at (\mytheta:4);
\path[draw,white] (-5,-2) -- (5,5);

\draw[] (1.75,0) arc [start angle=0, end angle=180, radius=1.75] -- (1.75,0) -- cycle;
\draw[dotted] (-1.75,0) arc [start angle=180, end angle=360, radius=1.75];

\draw[] (0,0) -- (90:4) arc [start angle=90, end angle=\mytheta, radius=4];

%%% VECTORS %%%
\draw[-Triangle] (0,0) -- (V2) node[pos=1,above] {$\va{q}$};
\draw[-Triangle] (0,0) -- (V1) node[pos=1,right] {$\va{p}$};

%%% GEOMETRY %%%
\fill[red,opacity=0.2] (0,0) -- ++(\mytheta:1.75) -- ++(0,4) -- ++(\mytheta+180:1.75);
\draw[] (0,0) -- ++(\mytheta:1.75) -- ++(0,4) -- ++(\mytheta+180:1.75);
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
    """
    Purpose:
        Makes an animation of the parallelogram dot product.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    animatetex.before_loop()
    for angle in np.linspace(0,180,numiter//2):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\mytheta}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    for angle in np.linspace(180,0,numiter//2):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\mytheta}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()