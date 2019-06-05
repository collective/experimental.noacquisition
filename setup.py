from setuptools import setup, find_packages


version = '1.0.0b5'

setup(name='experimental.noacquisition',
      version=version,
      description="No acquistion during publish traverse",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Zope2",
          "Programming Language :: Python",
      ],
      keywords='monkeypatch traverse',
      author='Mauro Amico',
      author_email='mauro.amico@gmail.com',
      url='http://pypi.org/pypi/collective/experimental.noacquisition',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['experimental', ],
      include_package_data=True,
      zip_safe=False,
      test_suite="experimental.noacquisition",
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'collective.monkeypatcher',
          'Zope2>=2.13.4,<=2.13.28'  # paranoid
      ],
      extras_require={
          'test': ['Products.CMFPlone[test]', 'Products.PloneTestCase']
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
