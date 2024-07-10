
import numpy as np
import Modules.animatetex as animatetex

numiter = 24

start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts}
\usepackage{tikz}
\usepackage{scalerel,pict2e,tkz-euclide,tikz-3dplot}
\usetikzlibrary{patterns,arrows.meta,calc,shadows,external}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\usetikzlibrary{perspective,spath3}
\usepackage{comment}
\begin{document}
'''

end = r'''
\begin{frame}
%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ANGULAR DEFINITIONS %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def \polar {65}
%\def \azimuth {130}
\def \myscale {1}
%\def \azimuth {0}
\tdplotsetmaincoords{\polar}{\azimuth}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% THE TIKZ ENVIRONMENT %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\begin{tikzpicture}[tdplot_main_coords, scale=\myscale]

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% COORDINATE AXES AND GRID %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\draw[-latex] (-4,0,0) -- (4,0,0) node[pos=1,below left]{$x$};
\draw[-latex] (0,-4,0) -- (0,4,0) node[pos=1,below right]{$y$};
\draw[] (-3.75,-3.75) -- (-3.75,3.75) -- (3.75,3.75) -- (3.75,-3.75) -- cycle;
\foreach \x in {-3.75,-3.5,...,3.75}{
\draw[thin,dotted] (\x,-3.75) -- (\x,3.75);}
\foreach \y in {-3.75,-3.5,...,3.75}{
\draw[thin,dotted] (-3.75,\y) -- (3.75,\y);}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% BLANK OUT PARTS ON TOP %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\tdplotsetrotatedcoords{180}{0}{0}
\fill[tdplot_rotated_coords,white] ({cos(\azimuth)},{sin(\azimuth)}) arc [start angle=\azimuth, end angle={\azimuth+180}, radius=1] -- cycle;
\fill[tdplot_screen_coords,white] ({cos(0)},{sin(0)}) arc [start angle=0, end angle=180, radius=1] -- cycle;

%%%%%%%%%%%%%%%%%%%%%%
%%% RIEMANN SPHERE %%%
%%%%%%%%%%%%%%%%%%%%%%

% SCREEN CIRCLE
\draw[tdplot_screen_coords,thin] (1,0) arc [start angle=0, end angle=180,radius=1];
\draw[tdplot_screen_coords,densely dashed,thin] (1,0) arc [start angle=0, end angle=-180,radius=1];

%%% NORTH POLE %%%
\path[tdplot_screen_coords,spath/save=pathname] (0,0) circle [radius=0.045];
\path[fill,spath/use={pathname, transform={shift={(\myscale*0,\myscale*0,\myscale*1)}}}];

%%% XY-PLANE CIRCLE %%%
\tdplotsetrotatedcoords{0}{0}{0}
\draw[tdplot_rotated_coords,densely dashed,thin] (\azimuth:1) arc [start angle=\azimuth, end angle={\azimuth+180}, radius=1];
\draw[tdplot_rotated_coords] (\azimuth:1) arc [start angle=\azimuth, end angle={\azimuth-180}, radius=1];

\path[draw,white,tdplot_screen_coords] (-5.5,-4.5) rectangle (5.5,4.5); 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\end{tikzpicture}
\end{frame}
\end{document}
'''


def main():
    animatetex.before_loop()
    for angle in np.linspace(0+120,30+120,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\def \azimuth {' + f'{angle}' + '}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()