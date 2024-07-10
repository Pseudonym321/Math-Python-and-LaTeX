
import Modules.animatetex as animatetex

preamble = r"""
\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
"""
postscript = r"""
\begin{document}
\centering
\begin{tikzpicture}[scale=2]
\foreach \Vs in {0}{
\foreach \Vt in {1,2,...,\Vnmo}{
%%% ORIGINAL VECTORS %%%
\draw[-latex] ({cos(90+(\Vs*360/\Vn))},{sin(90+(\Vs*360/\Vn))}) -- ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))});
%%% FRAME %%%
\draw[] ({cos(90+(\Vt*360/\Vn))},{sin(90+(\Vt*360/\Vn))}) -- ({cos(90+((\Vt+1)*360/\Vn))},{sin(90+((\Vt+1)*360/\Vn))});}}

\draw[white] (-2,-2) rectangle (2,2);
\end{tikzpicture}
\end{document}
"""

def main():
    animatetex.before_loop()
    for angle in range(3,12,1):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(preamble)
            new_line = r"\def \Vn {" + f"{angle}" + "}\n"
            tex.write(new_line)
            new_line = r"\def \Vnmo {" + f"{angle-1}" + "}\n"
            tex.write(new_line)
            tex.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()