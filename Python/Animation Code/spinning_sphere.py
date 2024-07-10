
import numpy as np
import Animation_Modules.animatetex as animatetex

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
\centering
\def \myscale {1}
\tdplotsetmaincoords{65}{\azimuth}
\begin{tikzpicture}[tdplot_main_coords,scale=\myscale]
\draw[tdplot_screen_coords] (0,0) circle [radius=1];
\foreach \t in {0, 10, ..., 350}{
\begin{scope}
%\clip[] (-2,-2,0) rectangle (2,2,2);
\tdplotsetrotatedcoords{90}{\t}{0}
\draw[tdplot_rotated_coords,very thin] (0,0) circle [radius=1];
\tdplotsetrotatedcoords{180}{90}{0}
\draw[tdplot_rotated_coords,very thin] (0,0,{sin(\t)}) circle [radius={cos(\t)}];
\end{scope}}
\clip[tdplot_screen_coords] (-5,-3) rectangle (5,3);
\draw[tdplot_screen_coords,white] (-4.9,-2.9) rectangle (4.9,2.9); 
\foreach \k in {10,20,...,80}{
%%% on C %%%
\draw[] ({1/cos(\k)},0) circle [radius={sqrt(1/(cos(\k)^2)-cos(\k))}];
\draw[] (0,{-sin(\k)/cos(\k)}) circle [radius={1/cos(\k)}];
}
\foreach \k in {100,110,...,170}{
%%% on C %%%
\draw[] ({1/cos(\k)},0) circle [radius={sqrt(1/(abs(cos(\k))^2)-abs(cos(\k)))}];
\draw[] (0,{-sin(\k)/cos(\k)}) circle [radius={1/cos(\k)}];
}
\draw[] (0,0) circle [radius=1];
\draw[] (0,-7,0) -- (0,7,0); % circle at infinity
\draw[] (-7,0,0) -- (7,0,0); % circle at infinity

%%% axes %%%
\draw[-latex,thick] (-2,0,0) -- (2,0,0) node[pos=1,below left]{$x,\xi$}; % x-axis
\draw[-latex,thick] (0,-3.5,0) -- (0,3.5,0) node[pos=1,below right]{$y,\eta$}; % y-axis
\draw[-latex,thick] (0,0,-2) -- (0,0,1.5) node[pos=1,above right]{$z,\zeta$}; % z-axis
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
    animatetex.before_loop()
    for angle in np.linspace(120,150,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\def \azimuth {' + f'{angle}' + '}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()