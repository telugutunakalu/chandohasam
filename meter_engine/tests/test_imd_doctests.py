# -*- coding: utf-8 -*-
"""Run the examples in every module docstring of indic_meter_dawg."""
import doctest
import importlib
import unittest

from imd_support import imd  # noqa: F401  (puts the package on sys.path)

MODULES = ["symbols", "ganas", "catalogue", "constraints", "grammar", "automaton", "builder",
           "walker", "parser", "stanza", "identify", "diagram", "docs", "prosody", "scansion"]


def load_tests(loader, tests, ignore):
    for name in MODULES:
        mod = importlib.import_module(f"indic_meter_dawg.{name}")
        tests.addTests(doctest.DocTestSuite(mod))
    return tests


if __name__ == "__main__":
    unittest.main()
