#!/usr/bin/env python

import setuptools

setup_params = dict(
        name='simplyrets',
        version="0.1",
        url='https://simplyrets.com',
        license='MIT',
        author='Christopher Reichert',
        author_email='christopher@simplyrets.com',
        description='SimplyRETS Listings API for Python',
        download_url='https://github.com/SimplyRETS/simplyrets-python-sdk/archive/v0.1.tar.gz',
        keywords=['simplyrets', 'rets api'],
        packages=setuptools.find_packages(),
    )

if __name__ == '__main__':
    setuptools.setup(**setup_params)
