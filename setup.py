#!/usr/bin/env python

import setuptools

setup_params = dict(
        name='simplyrets',
        version="0.1",
        description='SimplyRETS API for Python',
        author='Christopher Reichert',
        author_email='christopher@simplyrets.com',
        url='https://simplyrets.com',
        packages=setuptools.find_packages(),
    )

if __name__ == '__main__':
    setuptools.setup(**setup_params)
