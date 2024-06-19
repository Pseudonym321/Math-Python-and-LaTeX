import Riemann_integral as Ri
with open("TeX_file.tex", "w") as tex:
    preamble = r"""\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{tikz}
\begin{document}
\begin{frame}
\centering
\begin{tikzpicture}[scale=3]
\draw[thick,-latex] (-1.3,0) -- (1.3,0);
\draw[thick,-latex] (0,-0.3) -- (0,2.3);
\draw[domain=-1.23:1.18,smooth,variable=\Vt]
  plot (\Vt,{\Vt*\Vt*\Vt-0.5*\Vt+1},0);
\draw[] (-1,0) -- (-1,2) node[pos=1,above]{$a$};
\draw[] (1,0) -- (1,2) node[pos=1,above]{$b$};
"""
    postscript = r"""\end{tikzpicture}
\end{frame}
\end{document}"""
    for num in range (5,27):
        tex.write(preamble)
        delta, inputs = Ri.Riemann_sum(-1,1,num)
        for input in inputs:
            new_line = f"\\draw[] ({input},0) -- ({input},{{{input}^3-0.5*{input}+1}}) -- \n"
            tex.write(new_line)
        tex.write(postscript)
    