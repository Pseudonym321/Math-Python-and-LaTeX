
import numpy as np
import os
import shutil
#i added this so i could save everything and make sure it was saved
r=2.0
L=8.0
linspace_amount = 38
numiter = 4
# x_input is synonymous with "A" from the diagram

def x_input_function(x_input):
    return (2*x_input*r*np.abs((L**2)/(x_input**2+L**2))**(1/2))/np.abs(x_input**2+L**2)**(1/2)


x_input_list = [x_input_function(x_input) for x_input in np.linspace(-10,10,linspace_amount)]

def y_input_function_upper(x_input):
    return (np.abs(r**2-x_input**2)**(1/2)+L-r)

def y_input_function_lower(x_input):
    return (-np.abs(r**2-x_input**2)**(1/2)+L-r)


y_input_list = [y_input_function_upper(x_input) for x_input in x_input_list[:int(0.1*linspace_amount)]]
y_input_list.extend([y_input_function_lower(x_input) for x_input in x_input_list[int(0.1*linspace_amount):int(0.9*linspace_amount)]])
y_input_list.extend([y_input_function_upper(x_input) for x_input in x_input_list[int(0.9*linspace_amount):]])

# https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
import math

def rotate_x(x,y,theta): #rotate x,y around xo,yo by theta (rad)
    xr=math.cos(theta)*(x-0)-math.sin(theta)*(y-(L-r)) + 0
    return xr
def rotate_y(y,x,theta):
    yr=math.sin(theta)*(x-0)+math.cos(theta)*(y-(L-r))  + (L-r)
    return yr

rotated_x_list = []
rotated_y_list = []

def rotate(angle):
    global rotated_x_list,rotated_y_list
    rotated_x_list.clear()
    rotated_y_list.clear()
    for pos in range(len(x_input_list)):
        rotated_x_list.append(rotate_x(x_input_list[pos], y_input_list[pos],angle))
        rotated_y_list.append(rotate_y(y_input_list[pos], x_input_list[pos],angle))



'''
import matplotlib.pyplot as plt
x = x_input_list
y = y_input_list
plt.scatter(x, y, c ="blue")
# To show the plot
plt.show()
'''


#from matplotlib.widgets import Button, Slider
'''
rotate(0*np.pi/180)

import matplotlib.pyplot as plt
x = rotated_x_list
y = rotated_y_list
plt.scatter(x, y, c ="blue")
# To show the plot
plt.show()
'''

start= r'''
\documentclass{beamer}
\usepackage{tikz}
\begin{document}
\vspace*{\fill}
\begin{center}
\begin{tikzpicture}[scale=0.5]
\clip[] (-10,-1) rectangle (10,9);
\draw[black,-latex,thick] (0,-1) -- (0,9); % y-axis
\draw[black,-latex,thick] (-10,0) -- (10,0); % x-axis
\draw[] (0,6) circle [radius=2];
'''
end = r'''
\end{tikzpicture}
\end{center}
\vspace*{\fill}
\end{document}
'''


def draw_path(x,y):
    if np.abs((-L*x)/(y-L)) < 40:
        return r'''\draw[] (0,8) -- ({},0);
\fill[] ({},{}) circle [radius=0.08];
'''.format((-L*x)/(y-L),x,y)
    else:
        return r'''\draw[] (0,8) -- (0,0);
'''


def make_tikz_code():
    string = r''
    string += start
    for pos in range(len(x_input_list)):
        try:
            string += draw_path(rotated_x_list[pos], rotated_y_list[pos])
        except:
            pass
    string += end
    return string


rotate(-10*np.pi/180)
print(make_tikz_code())


from pypdf import PdfReader, PdfWriter

def remove_first_page(input_pdf, output_pdf):
    pdf_reader = PdfReader(input_pdf)
    pdf_writer = PdfWriter()

    # Add all pages except the first one
    for page_num in range(1, len(pdf_reader.pages)):
        pdf_writer.add_page(pdf_reader.pages[page_num])

    with open(output_pdf, 'wb') as output_file:
        pdf_writer.write(output_file)


import subprocess

output_directory = r''

# Function to compile a TeX file to PDF
def compile_tex_to_pdf(tex_file):
    subprocess.run(['pdflatex', tex_file])

# Function to append two PDF files
def append_pdfs(pdf1, pdf2, output_pdf):
    subprocess.run(['gswin64c', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, os.path.abspath(pdf1), os.path.abspath(pdf2)])
    #subprocess.run(['mgs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite', '-sOutputFile=' + output_pdf, pdf1, pdf2])

# Number of iterations for the loop
num_iterations = numiter

# Initial PDF file
merged_pdf = os.path.join(output_directory, 'merged_output.pdf') # make this the first frame

for i in range(0, num_iterations + 1):
    # Create a TeX file for each iteration
    tex_file = 'file_{}.tex'.format(1)
    rotate((i*10)*np.pi/180)
    string = make_tikz_code()
    with open(tex_file, 'w') as f:
        f.write(string)

    # Compile the TeX file to PDF
    compile_tex_to_pdf(tex_file)
    if i>1:
        # Append the generated PDF to the merged PDF
        temp_pdf = os.path.join(output_directory, 'merged_output_temp.pdf')
        append_pdfs(merged_pdf, 'file_{}.pdf'.format(i), temp_pdf)

        # Rename the temporary merged PDF to the original merged PDF
        shutil.move(temp_pdf, merged_pdf)
        #subprocess.run(['mv', 'merged_output_temp.pdf', merged_pdf])

remove_first_page(merged_pdf, os.path.join(output_directory, 'final_output.pdf'))

# Clean up - remove individual TeX and PDF files
for i in range(0, num_iterations + 1):
    try:
        os.remove('file_{}.tex'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.pdf'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.aux'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.log'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.nav'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.out'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.snm'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found
    try:
        os.remove('file_{}.toc'.format(i))
    except FileNotFoundError:
        pass  # Ignore if the file is not found



print('Cleaned up temporary files.')
print('Merged PDF file:', merged_pdf)



