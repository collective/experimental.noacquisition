from setuptools import setup, find_packages


version = "2.0.0b1.dev0"

setup(
    name="experimental.noacquisition",
    version=version,
    description="No acquistion during publish traverse",
    long_description="\n".join([open("README.rst").read(), open("CHANGES.rst").read()]),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Zope :: 5",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: 6.2",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="traverse acquisition",
    author="Mauro Amico",
    author_email="mauro.amico@gmail.com",
    url="http://pypi.org/pypi/collective/experimental.noacquisition",
    license="BSD",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=[
        "experimental",
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    test_suite="experimental.noacquisition",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        # explicitacquisition was added in Products.CMFCore 3.1
        "Products.CMFCore>=3.1",
    ],
    extras_require={"test": ["Products.CMFPlone[test]"]},
    entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
