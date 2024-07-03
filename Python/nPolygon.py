
import subprocess
import Modules.animatetex as animatetex
preamble = r"""
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
"""
postscript = r"""
\begin{document}
\centering
\begin{tikzpicture}[scale=2.5]
\foreach \Vt in {0,1,...,\Vn}{
\draw[] (0,0) -- ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))});
\draw[] ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))}) -- ({cos(90+((\Vt+1)*360/\Vn))},{sin(90+((\Vt+1)*360/\Vn))});
}

\draw[white] (-1.5,-1.5) rectangle (1.5,1.5);

\end{tikzpicture}
\end{document}"""

def main():
    animatetex.before_loop()
    for angle in range(3,28,1):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(preamble)
            new_line = f"\\newcommand{{\\Vn}}{{{angle}}}\n"
            tex.write(new_line)
            tex.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()