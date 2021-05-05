from setuptools import setup, find_namespace_packages

setup(
    name='clean_folder',
    version='1.0',
    description='Clean folder script',
    author='Khodyka Hanna',
    author_email='anna.khodyka@gmail.com',
    packages=find_namespace_packages(),
    #install_requires=['markdown'],
    entry_points={'console_scripts': ['clean_folder=clean_folder.clean:main']}
)