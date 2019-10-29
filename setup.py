import setuptools

if __name__ == '__main__':
    setuptools.setup(
        name='ncrbinary',
        version='0.1',
        packages=setuptools.find_packages(),

        install_requires=['crccheck>=0.6']
    )
