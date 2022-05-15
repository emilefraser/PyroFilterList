import setuptools

with open("README.org", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unbound-blocklist-generator",
    version="0.0.1",
    author="Jos van Bakel",
    author_email="jos@codeaddict.org",
    description="Unbound blocklist generator",
    long_description=long_description,
    long_description_content_type="text/x-org",
    url="https://github.com/c0deaddict/unbound-blocklist-generator",
    packages=['unbound_blgen'],
    entry_points={
        'console_scripts': [
            'unbound_blgen = unbound_blgen.__main__:main'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
