from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    setup(
        name='dango',
        version='0.0.1a',
        description='An easy to use tokenizer for Japanese text, aimed at language learners and non-linguists',
        long_description=fh.read(),
        long_description_content_type="text/markdown",
        url='https://github.com/mkartawijaya/dango',
        author='Martin Kartawijaya',
        author_email='pypi@m.kartawijaya.dev',
        license='BSD-3-Clause',
        packages=find_packages(include=['dango']),
        keywords=['japanese', 'tokenization', 'nlp'],
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: BSD License',
            'Topic :: Education',
            'Topic :: Text Processing :: Linguistic',
            'Natural Language :: Japanese'
        ],
        python_requires='>=3.6',
        install_requires=[
            'pygtrie ~= 2.4',
            'SudachiPy ~= 0.5.2',
            'SudachiDict-core >= 20210608',
        ],
        extras_require={
            'dev': [
                'build ~= 0.7',
                'twine ~= 3.6',
                'mypy ~= 0.910',
                'flake8 ~= 4.0'
            ],
            'test': [
                'pytest ~= 6.2',
                'coverage ~= 6.1',
            ]
        },
        entry_points={
            'console_scripts': ['dango=dango.cli:main']
        }
    )
