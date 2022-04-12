import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as fp:
    install_requires = fp.read()

setuptools.setup(
    name="global-land-mask",
    version="1.0.0",
    author="toddkarin",
    author_email="pvtools.lbl@gmail.com",
    description="Check whether a lat/lon point in on land or on sea",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/toddkarin/global-land-mask",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
