import os

from setuptools import find_packages, setup

try:
    readme = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
except:
    readme = ""

version = "0.2.13"

install_requires = [
    "djangorestframework",
]

extras_require = []

tests_require = [
    "factory_boy",
    "fake-factory",
    "pytest",
    "pytest-django",
    "pytest-cov",
    "tox",
]

setup(
    name="django-rest-framework-tricks",
    version=version,
    description="Collection of various tricks for Django REST framework.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Environment :: Web Environment",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
        "Framework :: Django",
        "Framework:: Django:: 2.2",
        "Framework:: Django:: 3.0",
        "Framework:: Django:: 3.1",
        "Framework:: Django:: 3.2",
        "Framework:: Django:: 4.0",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
    ],
    keywords="django, django rest framework, tricks",
    author="Artur Barseghyan",
    author_email="artur.barseghyan@gmail.com",
    url="https://github.com/barseghyanartur/django-rest-framework-tricks/",
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/"
        "django-rest-framework-tricks/",
        "Documentation": "https://django-rest-framework-tricks.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/"
        "django-rest-framework-tricks/",
        "Changelog": "https://django-rest-framework-tricks.readthedocs.io/"
        "en/latest/changelog.html",
    },
    package_dir={"": "src"},
    packages=find_packages(where="./src"),
    license="GPL-2.0-only OR LGPL-2.1-or-later",
    install_requires=(install_requires + extras_require),
    tests_require=tests_require,
    include_package_data=True,
)
