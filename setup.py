import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

properties = {}
with open('checkout_sdk/properties.py') as p:
    exec(p.read(), properties)

setuptools.setup(
    name='checkout_sdk',
    version=properties['VERSION'],
    author='Checkout.com',
    author_email='support@checkout.com',
    description='Checkout.com Python SDK',
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=False,
    url='https://github.com/checkout/checkout-sdk-python',
    license='MIT',
    packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'requests == 2.27.1'
    ],
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
