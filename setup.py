#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name="Mallet_LLDB",
      version="1.0a1",
      description="LLDB additions for iOS project.",
      url="https://github.com/bartoszj/Mallet",
      author="Bartosz Janda",
      license="MIT",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Environment :: MacOS X",
          "Environment :: Plugins",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: MacOS",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Debuggers"
      ],
      keywords="LLDB debugger development iOS summary",
      packages=find_packages(),
      install_requires=["PyYAML"],
      extras_require={
          "dev": ["tabulate"]
      },
      package_data={
          "mallet": ["config.yml"],
          "mallet.AFNetworking": ["config.yml", "lldbinit"],
          "mallet.CFNetwork": ["config.yml", "lldbinit", "class_dumps/*.json"],
          "mallet.common": ["config.yml", "lldbinit"],
          "mallet.CoreGraphics": ["config.yml", "lldbinit"],
          "mallet.debug_commands": ["config.yml", "lldbinit"],
          "mallet.Foundation": ["config.yml", "lldbinit", "class_dumps/*.json"],
          "mallet.QuartzCore": ["config.yml", "lldbinit", "class_dumps/*.json"],
          "mallet.StoreKit": ["config.yml", "lldbinit", "class_dumps/*.json"],
          "mallet.UIKit": ["config.yml", "lldbinit", "class_dumps/*.json"],
      })
