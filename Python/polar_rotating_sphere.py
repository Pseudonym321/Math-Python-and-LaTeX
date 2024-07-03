import Modules.animatetex as animatetex
numiter = 24
preamble = r"""
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
%%% PACKAGES %%%
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
%%% DEFINITIONS %%%
\newcommand{\Vazi}{120}
"""
postscript = r"""
\begin{document}
\begin{frame}
\centering
\tdplotsetmaincoords{50}{120}
\begin{tikzpicture}[tdplot_main_coords]
%%% OUTTER ELLIPSE %%%
\draw[very thin,tdplot_screen_coords] (0,0,0) circle(1);
\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};
%%% FOREACH LOOP %%%
\foreach \Vthe in {0, 10, ..., 350}{
%%% LONGITUTE %%%
\tdplotsetrotatedcoords{\Vthe+\Vazi}{90}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle(1);
\path[draw,black,very thin,spath/use={pathname, transform={shift={({0},{0},{0})}}}];
%%% LATITUTE %%%
\tdplotsetrotatedcoords{\Vazi}{\Vpol}{0}
\path[tdplot_rotated_coords,very thin,spath/save=pathname] (0,0,0) circle [radius={cos(\Vthe)}];
\path[tdplot_rotated_coords,draw,blue,very thin,spath/use={pathname, transform={shift={({0},{0},{sin(\Vthe)})}}}];
}
\end{tikzpicture}
\end{frame}
\end{document}"""

def main():
    animatetex.before_loop()
    for angle in range(0,360,360//numiter):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(preamble)
            tex.write(f"\\newcommand{{\\Vpol}}{{{angle}}}\n")
            tex.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()