from setuptools import setup, find_packages


version = '1.0.0b10'

setup(name='experimental.noacquisition',
      version=version,
      description="No acquistion during publish traverse",
      long_description=(open("README.rst").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          'Framework :: Zope2',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          'Framework :: Plone :: 5.1',
          'Framework :: Plone :: 5.2',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
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
          'Zope2>=2.13.4',
      ],
      extras_require={
          'test': ['Products.CMFPlone[test]']
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
