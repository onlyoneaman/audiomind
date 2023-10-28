from setuptools import setup, find_packages

setup(
    name='audiomind',
    include_package_data=True,
    version='0.0.1',
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
