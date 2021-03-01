import sys
import platform
import os

this_dir = os.path.realpath(os.path.dirname(__file__))
platform_name = '-'.join(('Python', platform.python_version(), platform.system()))
platform_dir = os.path.join(this_dir, platform_name)
if not platform_dir in sys.path:
    sys.path.append(platform_dir)
