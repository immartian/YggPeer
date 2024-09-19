from setuptools import setup, find_packages

setup(
    name="yggpeer",
    version="0.1.1",
    author="Isaac Mao",
    author_email="im@here.news",
    description="Peer-to-peer communication library over Yggdrasil",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/immartian/yggpeer", 
    packages=find_packages(),  # Automatically finds the packages in yggpeer/
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  
)
