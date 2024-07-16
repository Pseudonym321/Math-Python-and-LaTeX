
import numpy as np
import Animation_Modules.animatetex as animatetex

numiter = 24*2

start = r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz,tikz-3dplot}
\usetikzlibrary{spath3}
\begin{document}
\begin{frame}
\centering
'''

end = r'''
\tdplotsetmaincoords{45}{120}
\begin{tikzpicture}[tdplot_main_coords]
\def \Vn {270}
\def \Voo {60}
\draw[white,tdplot_screen_coords] (-5,-3.5) rectangle (5,3.5);
\clip[tdplot_screen_coords] (-5,-3.5) rectangle (5,3.5);
\draw[domain=90:\Vn,smooth,very thin,samples=500,variable=\Vt] plot (
{(\Vt/360)/(1-sqrt(1-(\Vt/360)^2)*cos(\Vo*\Vt))*sin(\Voo*\Vt)},
{(\Vt/360)/(1-sqrt(1-(\Vt/360)^2)*cos(\Vo*\Vt))*cos(\Voo*\Vt)},
{sin(\Vo*\Vt)/(1-sqrt(1-(\Vt/360)^2)*cos(\Vo*\Vt)))});
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
    """
    Purpose:
        Makes an animation of the cross and dot products.
    Parameters:
        No parameters.
    Return:
        Void.
    """
    animatetex.before_loop()
    for vo in np.linspace(8.5,11.5,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\def \Vo {' + f'{vo}' + r'}')
            f.write(end)
        animatetex.during_loop()
    for vo in np.linspace(11.5,8.5,numiter):
        with open(animatetex.TeX_file, 'w') as f:
            f.write(start)
            f.write(r'\def \Vo {' + f'{vo}' + r'}')
            f.write(end)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()