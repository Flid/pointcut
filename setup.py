from setuptools import find_packages, setup

setup(
    name='pointcut',
    version='0.1.0',
    description="TODO",
    license="Apache Software License (Apache 2.0)",
    long_description='TODO',
    long_description_content_type="text/markdown",
    url="https://github.com/TODO",
    python_requires=">=3.5",
    packages=find_packages(exclude=["tests*"]),

    tests_require=['pytest'],
    install_requires=[],
    author="Anton Kirilenko <antony.kirilenko@gmail.com>",
)
