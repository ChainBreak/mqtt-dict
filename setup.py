import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mqtt-dict", # Replace with your own username
    version="0.0.1",
    author="Thomas Rowntree",
    author_email="thomas.james.rowntree@gmail.com",
    description="A Python module that wraps a MQTT client into a magical dictionary!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ChainBreak/mqtt-dict",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)