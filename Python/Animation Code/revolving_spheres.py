
import numpy as np
import Animation_Modules.animatetex as animatetex

numiter = 24
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
\newcommand{\myscale}{0.66}
\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{30}{30}
\begin{tikzpicture}[tdplot_main_coords, scale=\myscale]
%%% FRAME %%%
\draw[white,tdplot_screen_coords] (0,0,0) circle(7);

%%% SPHERE 1 %%%
\draw[tdplot_screen_coords,very thin] (0,0,0) circle [radius=1];
\foreach \Vt in {0, 10, ..., 350}{
\tdplotsetrotatedcoords{0}{\Vt}{0}
\draw[tdplot_rotated_coords,very thin] (0,0,0) circle [radius=1];
\tdplotsetrotatedcoords{90}{90}{0}
\draw[tdplot_rotated_coords,very thin] (0,0,{sin(\Vt)}) circle [radius={cos(\Vt)}];}

%%% SPHERE 2 %%%
'''
end = r'''
\draw[very thin] ({5*cos(\Vn)},0,{5*sin(\Vn)}) circle [radius=1];
\foreach \Vt in {0, 10, ..., 350}{
\tdplotsetrotatedcoords{0}{\Vt}{0}
\path[tdplot_rotated_coords,spath/save=pathname] (0,0,0) circle [radius={1}];
\path[draw,spath/use={pathname, transform={shift={({\myscale*5*cos(\Vn)},{\myscale*0},{\myscale*5*sin(\Vn)})}}}];
\tdplotsetrotatedcoords{90}{90}{0}
\path[tdplot_rotated_coords,spath/save=pathname] (0,0,0) circle [radius={cos(\Vt)}];
\path[draw,spath/use={pathname, transform={shift={({\myscale*5*cos(\Vn)},{\myscale*sin(\Vt)},{\myscale*5*sin(\Vn)})}}}];
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
            f.write(r'\newcommand{\Vn}{' +f'{angle}' +'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()