
import numpy as np
import Animation_Modules.animatetex as animatetex

numiter = 24*3

start= r'''
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
'''
end = r'''
\begin{document}
\begin{frame}
\centering
\begin{tikzpicture}[scale=0.3]
\draw[white] (-11,-11) rectangle (11,11);
\coordinate (O) at (0,0);
\coordinate (A) at (1*\Vangle:4);
\coordinate (B) at (-2*\Vangle:3);
\coordinate (C) at (3*\Vangle:2);
\coordinate (D) at (-4*\Vangle:1);
\draw[] (O) -- (A) -- ++(B) -- ++(C) -- ++(D);
\draw[] (O) -- (A) -- ++(B) -- ++(D) -- ++(C);
\draw[] (O) -- (A) -- ++(C) -- ++(B) -- ++(D);
\draw[] (O) -- (A) -- ++(C) -- ++(D) -- ++(B);
\draw[] (O) -- (A) -- ++(D) -- ++(B) -- ++(C);
\draw[] (O) -- (A) -- ++(D) -- ++(C) -- ++(B);

\draw[] (O) -- (B) -- ++(A) -- ++(C) -- ++(D);
\draw[] (O) -- (B) -- ++(A) -- ++(D) -- ++(C);
\draw[] (O) -- (B) -- ++(C) -- ++(A) -- ++(D);
\draw[] (O) -- (B) -- ++(C) -- ++(D) -- ++(A);
\draw[] (O) -- (B) -- ++(D) -- ++(A) -- ++(C);
\draw[] (O) -- (B) -- ++(D) -- ++(C) -- ++(A);

\draw[] (O) -- (C) -- ++(A) -- ++(B) -- ++(D);
\draw[] (O) -- (C) -- ++(A) -- ++(D) -- ++(B);
\draw[] (O) -- (C) -- ++(B) -- ++(A) -- ++(D);
\draw[] (O) -- (C) -- ++(B) -- ++(D) -- ++(A);
\draw[] (O) -- (C) -- ++(D) -- ++(A) -- ++(B);
\draw[] (O) -- (C) -- ++(D) -- ++(B) -- ++(A);

\draw[] (O) -- (D) -- ++(A) -- ++(B) -- ++(C);
\draw[] (O) -- (D) -- ++(A) -- ++(C) -- ++(B);
\draw[] (O) -- (D) -- ++(B) -- ++(A) -- ++(C);
\draw[] (O) -- (D) -- ++(B) -- ++(C) -- ++(A);
\draw[] (O) -- (D) -- ++(C) -- ++(A) -- ++(B);
\draw[] (O) -- (D) -- ++(C) -- ++(B) -- ++(A);
\end{tikzpicture}
\end{frame}
\end{document}
'''

def main():
  """
    Purpose:
        Makes an animation of the cross product of a fixed vector and another one which
        follows the trajectory of a loxodrome.
    Parameters:
        No parameters.
    Return:
        Void.
    """
  animatetex.before_loop()
  for angle in np.linspace(0,360,numiter):
      with open(animatetex.TeX_file, 'w') as f:
          f.write(start)
          f.write(r'\newcommand{\Vangle}{' +f'{angle}' +'}\n')
          f.write(end)
      animatetex.during_loop()
  animatetex.after_loop()

if __name__ == "__main__":
    main()