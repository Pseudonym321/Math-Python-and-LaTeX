
import subprocess
import Modules.animatetex as animatetex

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
\tdplotsetmaincoords{45}{45}
\begin{tikzpicture}[tdplot_main_coords]
%%% OUTTER ELLIPSE %%%
\draw[very thin,tdplot_screen_coords] (0,0,0) circle(1);
\draw[-latex] (-3,0,0) -- (3,0,0) node[pos=1]{$x$};
\draw[-latex] (0,-3,0) -- (0,3,0) node[pos=1]{$y$};
\draw[-latex] (0,0,-3) -- (0,0,3) node[pos=1]{$z$};


\tdplotsetrotatedcoords{\Vazi}{\Vpol}{0}
\foreach \Vthe in {0, 10, ..., 170}{
%%% LONGITUTE %%%
\draw[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t] plot ({cos(\t)*sin(\Vthe)},{sin(\t)*sin(\Vthe)},{cos(\Vthe)});
%%% LATITUDE %%%
\draw[tdplot_rotated_coords,very thin,domain=0:360,smooth,variable=\t] plot ({cos(\t)*cos(\Vthe)},{cos(\t)*sin(\Vthe)},{sin(\t)});
}
\end{tikzpicture}
\end{frame}
\end{document}"""

def main():
    animatetex.before_loop()
    for angle in range(0,360,360//24):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(preamble)
            tex.write(f"\\newcommand{{\\Vpol}}{{{angle}}}\n")
            tex.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()