start = r"""line 1
line 2
line 3
"""

end = r"""
line 7
line 8
line 9
"""

with open("TeX_file.tex", "a+") as tex:
    tex.write(start)
    for line_number in range(4,7):
        if line_number != 6:
            tex.write(f"line {line_number}\n")
        else:
            tex.write(f"line {line_number}")
    tex.write(end)
    tex.seek(0)
    print(tex.read())