
import numpy as np
import Modules.animatetex as animatetex

numiter = 24

preamble= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''

postscript = r'''
\begin{document}
\centering
\tdplotsetmaincoords{45}{\Vazi}
\begin{tikzpicture}[tdplot_main_coords,scale=1]
\draw[tdplot_screen_coords,white] (-4.5,-3.5) rectangle (4.5,4.5);
\clip[tdplot_screen_coords] (-4.5,-3.5) rectangle (4.5,3.5);
\draw[-latex] (-10,0,0) -- (10,0,0) node[pos=1]{$x$};
\draw[-latex] (0,-10,0) -- (0,10,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,-10) -- (0,0,10) node[pos=1]{$z$};

\newcommand{\PSz}[2]{(cos(#2)*cos(#1))}
\newcommand{\PSy}[2]{(cos(#2)*sin(#1))}
\newcommand{\PSx}[2]{(sin(#2))}

\newcommand{\ASx}[2]{(sin(#1))}
\newcommand{\ASy}[2]{(cos(#1)*sin(#2))}
\newcommand{\ASz}[2]{(cos(#1)*cos(#2))}

\newcommand{\Lx}[1]{(#1/360)}
\newcommand{\Ly}[1]{(sqrt(1-(#1/360)^2)*cos(3*#1))}
\newcommand{\Lz}[1]{(sqrt(1-(#1/360)^2)*sin(3*#1))}

\newcommand{\SPx}[2]{((#1)/(1-#2))}
\newcommand{\SPy}[2]{((#1)/(1-#2))}


\foreach \Vk in {0,10,...,350}{
%%% POLAR %%%
\draw[domain=0:360,smooth,samples=50,variable=\Vt,blue]  plot ({\PSx{\Vt}{\Vk}},{\PSy{\Vt}{\Vk}},{\PSz{\Vt}{\Vk}});
%%% AZIMUTH %%%
\draw[domain=0:360,smooth,samples=50,variable=\Vt,blue]  plot ({\ASx{\Vt}{\Vk}},{\ASy{\Vt}{\Vk}},{\ASz{\Vt}{\Vk}});
}

\foreach \Vk in {10,20,...,80}{
%%% AZIMUTHAL PROJECTION %%%
\draw[domain=0:360,smooth,samples=500,variable=\Vt,blue] 
plot ({\SPx{\ASx{\Vt}{\Vk}}{\ASz{\Vt}{\Vk}}},{\SPy{\ASy{\Vt}{\Vk}}{\ASz{\Vt}{\Vk}}});
%%% POLAR PROJECTION %%%
\draw[domain=0:360,smooth,samples=500,variable=\Vt,blue] 
plot ({-\SPx{\PSx{\Vt}{\Vk}}{\PSz{\Vt}{\Vk}}},{\SPy{\PSy{\Vt}{\Vk}}{\PSz{\Vt}{\Vk}}});
}
\foreach \Vk in {100,110,...,170}{
%%% AZIMUTHAL PROJECTION %%%
\draw[domain=0:360,smooth,samples=500,variable=\Vt,blue] 
plot ({\SPx{\ASx{\Vt}{\Vk}}{\ASz{\Vt}{\Vk}}},{\SPy{\ASy{\Vt}{\Vk}}{\ASz{\Vt}{\Vk}}});
%%% POLAR PROJECTION %%%
\draw[domain=0:360,smooth,samples=500,variable=\Vt,blue] 
plot ({\SPx{\PSx{\Vt}{\Vk}}{\PSz{\Vt}{\Vk}}},{\SPy{\PSy{\Vt}{\Vk}}{\PSz{\Vt}{\Vk}}});
}

\draw[domain=-360:360,smooth,samples=50,variable=\Vt,red]  plot ({\Lx{\Vt}},{\Ly{\Vt}},{\Lz{\Vt}});
\draw[domain=-360:360,smooth,samples=5000,variable=\Vt,red] 
plot ({\SPx{\Lx{\Vt}}{\Lz{\Vt}}},{\SPy{\Ly{\Vt}}{\Lz{\Vt}}});

\end{tikzpicture}
\end{document}
'''

def main():
    """
    Purpose:
        Makes a spinning loxodrome projection.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    animatetex.before_loop()
    for theta in np.linspace(0+45,360+45,numiter):
        with open(animatetex.TeX_file, 'w') as TeX:
            TeX.write(preamble)
            TeX.write(r'\newcommand{\Vazi}{' +f'{theta}' +'}')
            TeX.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()