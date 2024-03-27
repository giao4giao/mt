#!/usr/bin/env python
# encoding: utf-8
import os

import unittest

suite = unittest.defaultTestLoader.discover('.')
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
