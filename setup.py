from setuptools import setup, find_packages

setup(
    name='blogsite',
    version='0.1',
    description='My Django application',
    packages=find_packages(),
    install_requires=[
        'asgiref==3.6.0',
        'autopep8==2.0.2',
        'certifi==2022.12.7',
        'charset-normalizer==3.1.0',
        'Django==4.2',
        'docopt==0.6.2',
        'idna==3.4',
        'Pillow==9.5.0',
        'pipreqs==0.4.13',
        'psycopg2-binary==2.9.6',
        'pycodestyle==2.10.0',
        'requests==2.28.2',
        'sqlparse==0.4.4',
        'urllib3==1.26.15',
        'yarg==0.1.9',
    ],
)
