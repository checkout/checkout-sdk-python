import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

constants = {}
with open(os.path.join('checkout_sdk', 'constants.py')) as f:
    exec(f.read(), constants)

setuptools.setup(
    name="checkout_sdk",
    version=constants['VERSION'],
    author="Checkout.com",
    author_email="support@checkout.com",
    description="Checkout.com Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    url="https://github.com/checkout/checkout-sdk-python",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests >= 2.0.0',
    ],
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)
