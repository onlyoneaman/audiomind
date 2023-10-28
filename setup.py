from setuptools import setup, find_packages

setup(
    name='audiomind',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # list of your dependencies, e.g.,
        'openai',
        'requests',
        'tiktoken',
        'openai-whisper',
        'langchain',
    ],
    entry_points={
        'console_scripts': [
            'audiomind=audiomind.main'
        ]
    }
)
