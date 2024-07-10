
import Modules.animatetex as animatetex
import numpy as np
numiter = 24
start= r'''
\documentclass{article}
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''
end = r'''
\begin{document}
\tdplotsetmaincoords{45}{\Vt}
\begin{tikzpicture}[tdplot_main_coords]
%%% AXES %%%

\draw[-latex] (0,0,0) -- (5,0,0) node[pos=1]{$x$};
\draw[-latex] (0,0,0) -- (0,5,0) node[pos=1]{$y$};
\draw[-latex] (0,0,0) -- (0,0,5) node[pos=1]{$z$};

\coordinate (A) at (1,-1,-1);
\coordinate (B) at (-1,1,-1);
\coordinate (C) at (-1,-1,1);
\coordinate (D) at (1,1,1);

%%% BLUE %%%
\draw[fill,opacity=0.3,blue] (A) -- (B) -- (D) -- cycle;
\draw[fill,opacity=0.3,red] (B) -- (D) -- (C) -- cycle;
\draw[fill,opacity=0.3,green] (D) -- (C) -- (A) -- cycle;
\draw[fill,opacity=0.3,black] (A) -- (B) -- (C) -- cycle;

%%% POINTS %%%
\path[tdplot_screen_coords,spath/save=point] (0,0,0) circle(0.1);
%%% INITIAL %%%
%\fill[blue][spath/use={point, transform={shift={({1},{2},{1})}}}]; %a

\end{tikzpicture}
\end{document}
'''

def main():
    animatetex.before_loop()
    for angle in np.linspace(0,360,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\newcommand{\Vt}{' +f'{angle}' +'}\n')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()