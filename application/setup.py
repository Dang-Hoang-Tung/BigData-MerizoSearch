#!/usr/bin/env python

from distutils.core import setup

setup(name='merizo_search_pipeline',
      version='1.0',
      description='Python code for the merizo search pipeline',
      author='Hoang Tung Dang',
      author_email='ucabhtd@ucl.ac.uk',
      url='TBC',
      packages=['pipeline'],
      install_requires=['einops', 'matplotlib', 'natsort', 'networkx', 'numpy<2.0', 'rotary_embedding_torch', 'scipy', 'setuptools', 'torch==2.0.1']
     )
