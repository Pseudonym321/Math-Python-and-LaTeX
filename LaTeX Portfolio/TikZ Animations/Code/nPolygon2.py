
import subprocess
import Animation_Modules.animatetex as animatetex
def latex(n):
    LaTeX = r"""
    \documentclass{beamer}
    \beamertemplatenavigationsymbolsempty
    \usepackage{tikz}
    \begin{document}
    \centering
    \begin{tikzpicture}[scale=1]
    """

    big_draw = r""
    for i in range(1,n+1):
        big_draw += r"\draw[-latex] (0,0) -- ({cos(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))},{sin(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))});" +"\n"
        big_draw += r"\draw[] ({cos(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))},{sin(90+(" + f"{i}" + r"*360/" + f"{n}" + r"))}) -- ({cos(90+((" + f"{i}" + r"+1)*360/" + f"{n}" + r"))},{sin(90+((" + f"{i}" + r"+1)*360/" + f"{n}" + r"))});" +"\n"
    LaTeX += big_draw
    big_draw = r"""
    \draw[] (0,0) -- ({cos(90)},{sin(90)})
    """
    for i in range(1,n+1):
        big_draw += r" -- ++({cos(90+((" + f"{i}" + r")*360/" + f"{n}" + r"))},{sin(90+((" + f"{i}" + r")*360/" + f"{n}" + r"))})" +"\n"
    big_draw += ";\n"
    LaTeX += big_draw

    LaTeX += r"""
    \draw[white] (-3,-3) rectangle (3,3);
    \end{tikzpicture}
    \end{document}
    """
    return LaTeX

def main():
    animatetex.before_loop()
    for angle in range(2,14,1):
        with open(animatetex.TeX_file, "w") as tex:
            tex.write(latex(angle))
        animatetex.during_loop()
    animatetex.after_loop()

if __name__ == "__main__":
    main()