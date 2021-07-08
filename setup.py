from setuptools import setup
import io



version={}
with open("trjtrypy/version.py") as fp:
    exec(fp.read(),version)

long_description=io.open('README.rst', encoding="utf-8").read()




setup(
    name="trjtrypy",
    version=version["__version__"],
    author="Hamed Khaiiate Ajami, Hasan Pourmahmood-Aghababa, Jeff M. Phillips",
    author_email="goldenstarcodeteam@gmail.com",
    description="Distance between trajectories",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/GoldenStarCode/trjtrypy",
    packages=["trjtrypy"],
    python_requires=">=3.7",
    install_requires=["numpy>=1.19.1","scipy>=1.6.3","matplotlib>=3.3.2"],
    license='MIT license',
    project_urls={
        'Bug Reports': 'https://github.com/GoldenStarCode/trjtrypy/issues',
        'Source': 'https://github.com/GoldenStarCode/trjtrypy/',
        'Documentation': 'https://github.com/GoldenStarCode/trjtrypy/blob/main/README.rst',
    },
    classifiers=[
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Topic :: Scientific/Engineering :: Mathematics',
    'Topic :: Scientific/Engineering :: Visualization',
],
)
