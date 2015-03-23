#!/usr/bin/env python

import setuptools

setup_params = dict(
        name='simplyrets',
        version="0.1",
        description='SimplyRETS API for Python',
        author='Christopher Reichert',
        author_email='christopher@simplyrets.com',
        url='https://simplyrets.com',
        download_url='https://github.com/simplyrets/simplyrets-python-sdk/tarball/0.1',
        keywords=['simplyrets', 'rets api']
        packages=setuptools.find_packages(),
    )

if __name__ == '__main__':
    setuptools.setup(**setup_params)
