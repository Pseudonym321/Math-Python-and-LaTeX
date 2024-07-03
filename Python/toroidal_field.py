
import numpy as np
import Modules.animatetex as animatetex
numiter = 24
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''
end = r'''
\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{40}{\Vtheta}
\begin{tikzpicture}[tdplot_main_coords]

%%% DEFINITIONS %%%
\def \Vazi {0}

%%% OUTTER ELLIPSE %%%
%\draw[very thin,tdplot_screen_coords] (0,0,0) circle(1);
%\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
%\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};


%%% FOREACH LOOP %%%
\foreach \Vthe in {0, 10, ..., 350}{
%%% LONGITUTE %%%
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle(1);
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
%%% LATITUTE %%%
\tdplotsetrotatedcoords{\Vazi}{90}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle [radius={cos(\Vthe)}];
\path[tdplot_rotated_coords,draw,very thin,spath/use={pathname, transform={shift={({0},{0},{sin(\Vthe)})}}}];
%%% MAGNETIC FIELD %%%
\foreach \Vdist in {20,40,60}{
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({1/cos(\Vdist)},0,0) circle({sqrt(1/(cos(\Vdist))^2-cos(\Vdist))});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
\tdplotsetrotatedcoords{\Vazi-90}{\Vthe}{90}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({-sin(\Vdist)/cos(\Vdist)},0,0) circle({1/cos(\Vdist)});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
\path[tdplot_rotated_coords,very thin,spath/save=pathname] ({sin(\Vdist)/cos(\Vdist)},0,0) circle({1/cos(\Vdist)});
\path[draw,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
}

}
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
    animatetex.before_loop()
    for angle in np.linspace(0,360,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\Vtheta}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()