import Modules.Riemann_integral as Ri
import Modules.animatetex as animatetex

preamble = r"""\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
\begin{document}
\begin{frame}
\centering
\begin{tikzpicture}[scale=3]
\draw[thick,-latex] (-1.3,0) -- (1.3,0);
%\draw[thick,-latex] (0,-0.3) -- (0,2.3);
\draw[domain=-1.23:1.18,smooth,variable=\Vt]
  plot (\Vt,{\Vt*\Vt*\Vt-0.5*\Vt+1},0);
\draw[] (-1,0) -- (-1,2) node[pos=1,above]{$a$};
\draw[] (1,0) -- (1,2) node[pos=1,above]{$b$};
"""
postscript = r"""\end{tikzpicture}
\end{frame}
\end{document}"""

def main():
    animatetex.before_loop()
    for num in range (5,30):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(preamble)
            delta, inputs = Ri.Riemann_sum(-1,1,num)
            for input in inputs:
                new_line = f"\\fill[blue, opacity=0.3] ({input},0) -- ({input},{{{input}^3-0.5*{input}+1}}) -- ++({delta},0) |- (0,0);\n"
                tex.write(new_line)
                new_line = f"\\draw[] ({input},0) -- ({input},{{{input}^3-0.5*{input}+1}}) -- ++({delta},0) |- (0,0);\n"
                tex.write(new_line)
            tex.write(postscript)
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()