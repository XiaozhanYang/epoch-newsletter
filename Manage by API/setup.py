from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Manage Email Campaign with Python'
LONG_DESCRIPTION = 'A package build on top of BeautifulSoup, Jinja, Mailchimp API. It can be used to send email campaigns by providing the links of source articles on epochtimes.com'

# setting up
setup(
    # the name must match the folder name
    name='pynewsletter',
    version=VERSION,
    author="Xiaozhan Yang",
    author_email="xiaozhan.yang@epochtimes.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['Jinja2','beautifulsoup4', 'mailchimp-marketing'],
    keywords=['python', 'newsletter'],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Business",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ]
)
