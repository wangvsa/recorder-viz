import setuptools

c_reader_module = setuptools.Extension('recorder_viz/librreader', ['lib/reader.c'])

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="recorder-viz",            # Package name, e.g., pip install recorder-viz
    version="0.0.4",
    author="Chen Wang",
    author_email="wangvsa@gmail.com",
    description="Utilities for processing Recorder traces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangvsa/recorder-viz",
    packages=['recorder_viz'],     # package for import: after installaion, import recorder_viz
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    ext_modules=[c_reader_module],
)
