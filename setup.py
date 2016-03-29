from distutils.core import setup
setup(
  name = 'aadb',
  packages = ['aadb'], # this must be the same as the name above
  version = '0.1',
  description = 'A tool to manage multiple Android devices connected to a host using Android Debug Bridge (adb)',
  author = 'Patrick Farrell',
  author_email = 'pfarrell85@gmail.com',
  url = 'https://github.com/pfarrell85/AndroidTools', # use the URL to the github repo
  download_url = 'https://github.com/pfarrell85/AndroidTools/tarball/0.1', # I'll explain this in a second
  keywords = ['Android', 'adb'], # arbitrary keywords
  classifiers = [],
)