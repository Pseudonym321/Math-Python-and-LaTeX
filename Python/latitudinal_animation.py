
import numpy as np
import Modules.animatetex as animatetex

numiter = 24
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%maths
\usepackage{mathtools}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsfonts}
\usepackage{autobreak}
\usepackage{comment}
%tikzpicture
\usepackage{tikz}
\usepackage{scalerel}
\usepackage{pict2e}
\usepackage{tkz-euclide}
\usepackage{tikz-3dplot}
\usetikzlibrary{calc}
\usetikzlibrary{patterns,arrows.meta}
\usetikzlibrary{shadows}
\usetikzlibrary{external}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\usetikzlibrary{perspective,spath3}

'''
end = r'''


\newcommand{\myscale}{2.1}
\begin{document}
\begin{frame}
\begin{tikzpicture}[scale=\myscale]
%%% GEOMETRY %%%
\draw[] (0,0) circle [radius=1];
\draw[] (0,0) -- (\mytheta:1);

%%% LINES %%%
\draw[] (0,1) -- ({cos(\mytheta)},{sin(\mytheta)});
\draw[] (0,1) -- ({cos(\mytheta)/(1-sin(\mytheta))},0);

\fill[] ({cos(\mytheta)/(1-sin(\mytheta))},0) circle [radius=0.05];
\draw[] ({cos(\mytheta)},{sin(\mytheta)}) -- ({cos(\mytheta)},{-sin(\mytheta)});
\fill[] ({cos(\mytheta)},{-sin(\mytheta)}) circle [radius=0.05];

\draw[] (0,1) -- ({cos(\mytheta)},{-sin(\mytheta)});
\draw[] (0,1) -- ({cos(\mytheta)/(1+sin(\mytheta))},0);
\fill[] ({cos(\mytheta)/(1+sin(\mytheta))},0) circle [radius=0.05];

\draw[thin,densely dotted] ({cos(\mytheta)/(1-sin(\mytheta))},0) -- ({cos(\mytheta)/(1-sin(\mytheta))},-1.3);
\draw[thin,densely dotted] ({cos(\mytheta)/(1+sin(\mytheta))},0) -- ({cos(\mytheta)/(1+sin(\mytheta))},-1.3);
\draw[|-|] ({cos(\mytheta)/(1-sin(\mytheta))},-1.3) -- ({cos(\mytheta)/(1+sin(\mytheta))},-1.3);



%%% AXES %%%
\draw[-latex,thick] (0,0) -- (0,2);
\draw[-latex,thick] (-1.5,0) -- (3,0);

%%% NODES %%%
\fill[] (0,0) circle [radius=0.05];
\fill[] (0,1) circle [radius=0.05];
%\fill[] (\mytheta+180:1) circle [radius=0.05];
\fill[] (\mytheta:1) circle [radius=0.05];
\draw[red,|-Latex] ({1/cos(\mytheta)},-1.5) -- ({1/cos(\mytheta)},0);
\end{tikzpicture}
\end{frame}
\end{document}
'''
def main():
    animatetex.before_loop()
    for angle in np.linspace(0,50,numiter//2):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\mytheta}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    for angle in np.linspace(50,0,numiter//2):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\mytheta}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()