
import numpy as np
import Modules.animatetex as animatetex

numiter = 24

start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts}
\usepackage{tikz,scalerel,pict2e}
\usepackage{tikz-3dplot,tkz-euclide}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\def \myscale {1}
\begin{document}
'''

end = r'''
\begin{frame}
%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% ANGULAR DEFINITIONS %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def \polar {65}
%\def \azimuth {130}
%\def \polar {0}
%\def \azimuth {180}
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

\tdplotsetrotatedcoords{90}{45}{0}
\path[tdplot_rotated_coords,spath/save=name] (0,0) circle [radius={sqrt(2)/2}];
\path[draw,spath/use={name, transform={shift={(\myscale*0,\myscale*0.5,\myscale*0.5)}}}];


%%%%%%%%%%%%%%%%%%%%%
%%% RED FOREACH %%%
%%%%%%%%%%%%%%%%%%%%%
\foreach \x in {0.25,0.5,...,3}{
\tdplotsetrotatedcoords{0}{{atan(1/\x)}}{0}
\path[tdplot_rotated_coords,spath/save=name] (0,0) circle [radius={sqrt(((2*\x)/(1+(\x)^2))^2+((-2)/(1+(\x)^2))^2)/2}];
\path[draw,red,spath/use={name, transform={shift={({\myscale*\x/(1+(\x)^2)},\myscale*0,{\myscale*((((\x)^2-1)/((\x)^2+1))+1)/2})}}}];}

%%%%%%%%%%%%%%%%%%%%%
%%% BLUE FOREACH %%%
%%%%%%%%%%%%%%%%%%%%%
\foreach \x in {0.25,0.5,...,3}{
\tdplotsetrotatedcoords{90}{{atan(1/\x)}}{0}
\path[tdplot_rotated_coords,spath/save=name] (0,0) circle [radius={sqrt(((2*\x)/(1+(\x)^2))^2+((-2)/(1+(\x)^2))^2)/2}];
\path[draw,blue,spath/use={name, transform={shift={(\myscale*0,{\myscale*\x/(1+(\x)^2)},{\myscale*((((\x)^2-1)/((\x)^2+1))+1)/2})}}}];}

%%%%%%%%%%%%%%%%%%%%%
%%% GREEN FOREACH %%%
%%%%%%%%%%%%%%%%%%%%%
\foreach \x in {0.25,0.5,...,3}{
\tdplotsetrotatedcoords{180}{{atan(1/\x)}}{0}
\path[tdplot_rotated_coords,spath/save=name] (0,0) circle [radius={sqrt(((2*\x)/(1+(\x)^2))^2+((-2)/(1+(\x)^2))^2)/2}];
\path[draw,green,spath/use={name, transform={shift={({\myscale*-\x/(1+(\x)^2)},\myscale*0,{\myscale*((((\x)^2-1)/((\x)^2+1))+1)/2})}}}];}


%%%%%%%%%%%%%%%%%%%%%
%%% YELLOW FOREACH %%%
%%%%%%%%%%%%%%%%%%%%%

\foreach \x in {0.25,0.5,...,3}{
\tdplotsetrotatedcoords{270}{{atan(1/\x)}}{0}
\path[tdplot_rotated_coords,spath/save=name] (0,0) circle [radius={sqrt(((2*\x)/(1+(\x)^2))^2+((-2)/(1+(\x)^2))^2)/2}];
\path[draw,yellow,spath/use={name, transform={shift={(\myscale*0,{\myscale*-\x/(1+(\x)^2)},{\myscale*((((\x)^2-1)/((\x)^2+1))+1)/2})}}}];}

\path[draw,white,tdplot_screen_coords] (-5.5,-4.5) rectangle (5.5,4.5); 
\end{tikzpicture}

\end{frame}

\end{document}

'''

def main():
    animatetex.before_loop()
    for angle in np.linspace(120,180,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\def \azimuth {' + f'{angle}' + '}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()