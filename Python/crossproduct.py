
import numpy as np
import Modules.animatetex as animatetex
numiter = 24
start = r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%maths
\usepackage{mathtools,amsmath,amssymb,amsfonts,physics}
\usepackage{tikz,scalerel,pict2e,ifthen}
\usepackage{tikz-3dplot,tkz-euclide}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
\def \p {1.75}
\def \q {4}
\begin{document}
\begin{frame}
'''

end = r'''
\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords,scale=0.7]
\coordinate (O) at (0,0);
\coordinate (V1) at (0:\p);
\coordinate (V2) at (\t:\q);
\path[draw,white] (-5,-5) -- (5,5);

\draw[] (\p,0) arc [start angle=360, end angle=180, radius=\p] -- (\p,0) -- cycle;
\draw[dotted] (-\p,0) arc [start angle=180, end angle=0, radius=\p];

\draw[] (0,0) -- (270:\q) arc [start angle=270, end angle=\t, radius=\q];

%%% VECTORS %%%
\draw[-Triangle] (0,0) -- (V2) node[pos=1,above] {$\va{q}$};
\draw[-Triangle] (0,0) -- (V1) node[pos=1,right] {$\va{p}$};

%%% GEOMETRY %%%
\fill[red,opacity=0.2] (0,0) -- ++(\t:\p) -- ++(0,-\q) -- ++(\t+180:\p);
\draw[] (0,0) -- ++(\t:\p) -- ++(0,-\q) -- ++(\t+180:\p) -- cycle;

\fill[blue,opacity=0.2] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q);
\draw[] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q) -- cycle;
\draw[blue,-Triangle] (0,0,0) -- (0,0,{\p*\q*sin(\t)}) node[left]{$\va{p}\cross\va{q}$};
\draw[white,tdplot_screen_coords] (-5,-6) rectangle (5,6);
\end{tikzpicture}
\end{frame}
\end{document}
'''

end2 = r"""
\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords,scale=0.7]
\coordinate (O) at (0,0);
\coordinate (V1) at (0:\p);
\coordinate (V2) at (\t:\q);
\path[draw,white] (-5,-5) -- (5,5);

\draw[] (\p,0) arc [start angle=0, end angle=180, radius=\p] -- (\p,0) -- cycle;
\draw[dotted] (-\p,0) arc [start angle=180, end angle=360, radius=\p];

\draw[] (0,0) -- (90:\q) arc [start angle=90, end angle=\t, radius=\q];

%%% VECTORS %%%
\draw[-Triangle] (0,0) -- (V2) node[pos=1,above] {$\va{q}$};
\draw[-Triangle] (0,0) -- (V1) node[pos=1,right] {$\va{p}$};

%%% GEOMETRY %%%
\fill[red,opacity=0.2] (0,0) -- ++(\t:\p) -- ++(0,\q) -- ++(\t+180:\p);
\draw[] (0,0) -- ++(\t:\p) -- ++(0,\q) -- ++(\t+180:\p) -- cycle;

\fill[blue,opacity=0.2] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q);
\draw[] (0,0) -- ++(\t:\q) -- ++(\p,0) -- ++(\t+180:\q) -- cycle;
\draw[blue,-Triangle] (0,0,0) -- (0,0,{\p*\q*sin(\t)}) node[left]{$\va{p}\cross\va{q}$};
\draw[white,tdplot_screen_coords] (-5,-6) rectangle (5,6);

\end{tikzpicture}
\end{frame}
\end{document}
"""

animatetex.before_loop()
for angle in np.linspace(0,360,numiter):
    with open(animatetex.TeX_file, 'w') as f:
        f.write(start)
        f.write(r'\def \t {' + f'{angle}' + r'}')
        if angle <= 180:  
            f.write(end2)
        else:
            f.write(end)
    animatetex.during_loop()
animatetex.after_loop()