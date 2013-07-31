from .utils import TestCase
from tempfile import mkdtemp
import itertools
import os
import sys

_module_name_generator = ("custom_module_{0}".format(x) for x in itertools.count())

class ExtHookTest(TestCase):
    def setUp(self):
        super(ExtHookTest, self).setUp()
        self.path = mkdtemp()
        self.addCleanup(setattr, sys, "path", list(sys.path))
        sys.path.insert(0, self.path)
        self.expected_value = 31337
        self.module_name = next(_module_name_generator)

        with open(os.path.join(self.path, "slash_{0}.py".format(self.module_name)), "w") as f:
            f.write("value = {0!r}".format(self.expected_value))

    def test_ext_hook_import(self):
        statement = "from slash.ext import {0} as module".format(self.module_name)
        exec(statement)
        self.assertEquals(module.value, self.expected_value)

    def test_ext_hook_import_nonexistent(self):
        with self.assertRaises(ImportError):
            from slash.ext import nonexistent
