import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oktadboto",
    version="0.0.3",
    author="Upserve",
    author_email="datascience@upserve.com",
    description="Boto3 RefreshableCredentials wrapping oktad system call",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    license="MIT",
    url="https://github.com/upserve/oktadboto",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["boto3"],
    extras_require={"dev": ["flake8", "black"]},
    python_requires="~=3.7",
)
