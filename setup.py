from setuptools.command.install import install
import setuptools
import subprocess

class my_install(install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', 'lib'])
        subprocess.call(['make', '-C', 'lib'])
        install.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="recorder-viz",            # Package name, e.g., pip install recorder-viz
    version="0.0.1",
    author="Chen Wang",
    author_email="wangvsa@gmail.com",
    description="Utilities for processing Recorder traces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wangvsa/recorder-utils",
    packages=['recorder_viz'],     # package for import: after installaion, import recorder_viz
    package_data={'recorder_viz': ['librreader.so']},
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: University of Illinois/NCSA Open Source License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
    cmdclass={'install': my_install},
)
