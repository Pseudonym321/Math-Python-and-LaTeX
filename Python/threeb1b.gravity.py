
import numpy as np
import Modules.animatetex as animatetex
numiter = 24
start = r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts}
\usepackage{tikz,scalerel,pict2e}
\usepackage{tikz-3dplot,tkz-euclide}
\usepackage{comment}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}


\begin{document}
\begin{frame}
'''
end = r'''
\begin{tikzpicture}[scale=0.3]
\path[name path=circle,draw] (0,0) circle [radius=5cm];
\path[fill] (3,0) circle [radius=0.2]; %replace with nodes?
\path[fill] (0,0) circle [radius=0.2];

\foreach \i in {1,2,...,24}
{
  \edef\optname{name path global=line\i}
  \expandafter\path\expandafter[\optname] (3,0) -- ++(15*\i:10);
  \path[name intersections={of=circle and line\i}] (intersection-1);
  \path[spath/save=name](3,0) -- (intersection-1);
  \path[draw,spath/use={name,transform={rotate around={\p:(spath cs:name .5)}}}=\name];
};
\draw[white] (-6,-6) rectangle (6,6);
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
    animatetex.before_loop()
    for angle in np.linspace(0,90,numiter//2):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\p}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()