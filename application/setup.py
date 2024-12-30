#!/usr/bin/env python

from distutils.core import setup

setup(name='merizo_search_pipeline',
      version='1.0',
      description='Python code for the merizo search pipeline',
      author='Hoang Tung Dang',
      author_email='ucabhtd@ucl.ac.uk',
      url='TBC',
      packages=['pipeline'],
      install_requires=['einops', 'matplotlib', 'natsort', 'networkx', 'numpy<2.0', 'rotary_embedding_torch', 'scipy', 'setuptools', 'https://download.pytorch.org/whl/cpu/torch-1.0.1-cp37-cp37m-linux_x86_64.whl#sha256=c612200fed3ef0d2243e3517d7cc529eadc2521c62ad1413a6558a6b6d2c3d33']
     )
