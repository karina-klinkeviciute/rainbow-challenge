import sys
import pathlib
import os
from dotenv import load_dotenv
load_dotenv()

this_directory = pathlib.Path(__file__).parent.absolute()
project_directory = os.path.join(this_directory, 'rainbow_project')
print('PROJECT DIRECTORY: ', project_directory)
sys.path.insert(0, project_directory)

import django; django.setup()
