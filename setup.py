from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    setup(
        name='dango',
        version='0.0.0a0',
        description='An easy to use tokenizer for Japanese text, aimed at language learners and non-linguists',
        long_description=fh.read(),
        long_description_content_type="text/markdown",
        url='https://github.com/mkartawijaya/dango',
        author='Martin Kartawijaya',
        author_email='pypi@m.kartawijaya.dev',
        license='BSD-3-Clause',
        packages=find_packages(),
        keywords=['japanese', 'tokenization', 'nlp'],
        classifiers=[
            'Development Status :: 1 - Planning',
            'License :: OSI Approved :: BSD License',
            'Topic :: Education',
            'Topic :: Text Processing :: Linguistic',
            'Natural Language :: Japanese'
        ],
        install_requires=[]
    )
