Python Coding Challenge

### Setup
1. Extract Zip File
Unzip the .zip file to a folder of your choice.

2. Virtual Environment
- Set up a virtual environment on your local machine
- Activate your virtual environment
> https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments

3. Change Directory
With your CLI, make sure you change your directory to the project folder.
example > cd your_path/MedaMonks_Assignment/project_folder

4. Install Required Packages
In the project_folder, find the requirements.txt file. Install them in your virtual environment.
> https://docs.python.org/3/tutorial/venv.html#managing-packages-with-pip

### Using the filter_image.py script

# Help
For information about the commands, use the following command:
> python filter_image.py --help

# Arguments
- The script takes two "REQUIRED" positional arguments, and three filters (optional arguments starting with '--')

positional arguments:
  input_image        REQUIRED - The input image file name which you want to apply filters to.
  output_image       REQUIRED - The file name you want to give to the outputted image. (only .jpg and .png extensions are supported)

optional arguments:
  -h, --help         show this help message and exit
  --gray_scale       Filter. Change color scheme of the image (as processed up to that point) to gray scale.
  --overlay OVERLAY  Filter. Overlay another image on top of the input image. Specify the name of the overlay.
  --rotate ROTATE    Filter. Rotate image by [N] degrees.

- The two optional arguments "--overlay" and "--rotate" take an additional parameter.
    for --overlay, specify the image file.
    > --overlay example.jpg
    for --rotate, specify the number of degrees to rotate the image.
    > --rotate 45
- The positional arguments may be used multiple times.
- The positional argument filters will be applied in order of input (chronologically).

# Usage
- Save images of your choice in the project_folder.
- start your command with
    > python filter_image.py
- In chronological order, extend this with any filters you wish to apply.
    > python filter_image.py --gray_scale --rotate -45 --overlay python.png input.jpg output.png
- The positional arguments "input_image" and "output_image" are required at the end of the command line.

NOTE: the filters are applied chronologically.
For instance, the command:
> python filter_image.py --gray_scale --overlay python.png input.jpg output.png
will only turn the input_image "input.jpg" into gray scale, but not the overlay image "python.png".

### Testing
in the cli, run the command:
> pytest







