import setuptools
from setuptools.command.build_ext import build_ext

c_reader_module = setuptools.Extension('recorder_viz/libreader',
                                        ['recorder_viz/reader.c'], include_dirs=['recorder_viz'])

class my_build_ext(build_ext):
    # The default implementation of this function adds some
    # libraries to the linker during the building process.
    # e.g ['python3.x']
    #
    # However, in many clusters such as Theta and BlueWaters,
    # the path of libpython.so is unkown to the build script
    # thus it will cuase errors.
    #
    # Therefore, we overwrite this function to avoid adding
    # additional libraries.
    def get_libraries(self, ext):
        return ext.libraries


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recorder-viz",                # Package name, e.g., pip install recorder-viz
    version="0.4.0",
    author="Chen Wang",
    author_email="wangvsa@gmail.com",
    description="Utilities for processing Recorder traces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangvsa/recorder-viz",
    packages=['recorder_viz'],                  # package for import: after installaion, import recorder_viz
    package_data = {'recorder_viz': ['*.h']},   # *.h by default will not be copied, we use this to ship it.
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    ext_modules=[c_reader_module],
    cmdclass={'build_ext': my_build_ext},
)

