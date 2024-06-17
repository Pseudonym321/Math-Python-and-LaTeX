preamble_beginning = r"""\documentclass{beamer}
\beamertemplatenavigationsymbolsempty
\usepackage{mathtools,amsmath,amssymb,amsfonts,physics}
\usepackage{tikz,scalerel,tikz-3dplot,tkz-euclide}
\usepackage{pict2e,ifthen}
\usetikzlibrary{calc,patterns,arrows.meta}
\usetikzlibrary{shadows,external,perspective,spath3}
\usetikzlibrary{decorations.pathreplacing,angles,quotes}
"""

postscript = r"""
line 7
line 8
line 9"""

with open("TeX_file.tex", "a+") as tex:
    tex.write(preamble_beginning)
    for line_number in range(4,7):
        if line_number != 6:
            tex.write(f"line {line_number}\n")
        else:
            tex.write(f"line {line_number}")
    tex.write(postscript)
    tex.seek(0)
    print(tex.read())