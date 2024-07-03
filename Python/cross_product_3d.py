
import numpy as np
import Modules.animatetex as animatetex
numiter = 24*5
start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
'''
end = r'''
\newcommand{\Pa}{0}
\newcommand{\Pb}{0}
\newcommand{\Pc}{0}
\newcommand{\Ua}{(-2)}
\newcommand{\Ub}{2}
\newcommand{\Uc}{1}
\newcommand{\Vr}{1.5}
\newcommand{\Va}{(\Vr*sin(4*\Vt)*(1-(\Vt/360)^2)^(0.5))}
\newcommand{\Vb}{(\Vr*(\Vt/360))}
\newcommand{\Vc}{(\Vr*cos(4*\Vt)*(1-(\Vt/360)^2)^(0.5))}
\begin{document}
\centering
\tdplotsetmaincoords{45}{120}
\begin{tikzpicture}[tdplot_main_coords,scale=0.75]
%%% AXES %%%
%\draw[-latex] (0,0,0) -- (5,0,0) node[pos=1]{$x$};
%\draw[-latex] (0,0,0) -- (0,5,0) node[pos=1]{$y$};
%\draw[-latex] (0,0,0) -- (0,0,5) node[pos=1]{$z$};

%%% POINTS %%%
\path[tdplot_screen_coords,spath/save=point] (0,0,0) circle(0.1);
%\fill[][spath/use={point, transform={shift={({-1},{0},{1})}}}];

%%% COORDINATES %%%
\coordinate (O) at (0,0,0);
\coordinate (P) at ({\Pa},{\Pb},{\Pc});
\coordinate (U) at ({\Pa+\Ua},{\Pb+\Ub},{\Pc+\Uc});
\coordinate (V) at ({\Pa+(\Va)},{\Pb+(\Vb)},{\Pc+(\Vc)});
\coordinate (UandV) at ({\Pa+(\Ua+\Va)},{\Pb+\Ub+\Vb},{\Pc+\Uc+\Vc});
\coordinate (CP) at ({\Pa+(\Ub*\Vc-\Uc*\Vb)},{\Pb-(\Ua*\Vc-\Uc*\Va)},{\Pc+(\Ua*\Vb-\Ub*\Va)});



\draw[domain=-360:360,very thin,smooth,samples=500,variable=\t]
  plot ({\Pa+\Vr*sin(4*\t)*(1-(\t/360)^2)^(0.5)},{\Pb+\Vr*\t/360},{\Pc+\Vr*cos(4*\t)*(1-(\t/360)^2)^0.5});


%%% VECTOR V %%%
\draw[thick,-latex] (O) -- ({\Va},{\Vb},{\Vc});

%%% VECTOR U %%%
\draw[thick,-latex] (O) -- ({\Ua},{\Ub},{\Uc});

%%% BLUE AREA %%%
\fill[blue,opacity=0.3] (O) -- (U) -- (UandV) -- (V);

%%% BLUE VECTOR %%%
\draw[blue,-latex,thick] (O) -- (CP);

\draw[white,tdplot_screen_coords] (-6,-6) rectangle (6,6);
\end{tikzpicture}
\end{document}
'''

animatetex.before_loop()
for angle in np.linspace(-360,360,numiter):
    with open(animatetex.TeX_file, 'w') as f:
        f.write(start)
        f.write(r'\newcommand{\Vt}{' +f'{angle}' +'}\n')
        f.write(end)
    animatetex.during_loop()
animatetex.after_loop()