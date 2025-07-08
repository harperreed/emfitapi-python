from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="emfitapi-python",
    version="0.1.0",
    author="Harper Reed",
    author_email="harper@nata2.org",
    description="A Python wrapper for the Emfit QS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/harperreed/emfitapi-python",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    include_package_data=True,  # This line ensures MANIFEST.in is used
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
