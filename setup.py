from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='audiomind',
    include_package_data=True,
    version='0.2.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'openai',
        'tiktoken',
        'openai-whisper',
        'langchain',
        'python-dotenv',
        'pydub',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'audiomind=audiomind.main:main'
        ]
    }
)
