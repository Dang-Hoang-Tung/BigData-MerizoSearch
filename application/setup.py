#!/usr/bin/env python

from distutils.core import setup

setup(name='MerizoSearchPipeline',
      version='1',
      description='Python code for parallel processing of Merizo Search results',
      author='Hoang Tung Dang',
      author_email='ucabhtd@ucl.ac.uk',
      url='TBC',
      packages=['pipeline'],
      # install_requires=['bs4','requests', 'mr4mp', 'lxml', 'minio'],
      # entry_points={'console_scripts': ['build-index = dataeng.gather:parse_index_entry',
                                    #     'analyse = dataeng.analysis:analysis_entry',
                                    #     'combine = dataeng.combine:combine_entry'
                                    #     ]}
     )
