#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2014 Bartosz Janda
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import lldb
import ClassDump
import LoadScripts
import Helpers
import TypeCache


class SummaryBase_SynthProvider(object):
    # SummaryBase:

    _architectures_list = None

    def __init__(self, value_obj, internal_dict):
        # self.as_super = super(SummaryBase_SynthProvider, self)
        # self.as_super.__init__()
        super(SummaryBase_SynthProvider, self).__init__()

        self.default_dynamic_type = lldb.eDynamicDontRunTarget
        # self.default_dynamic_type = lldb.eDynamicCanRunTarget

        self.value_obj = value_obj
        self.dynamic_value_obj = self.value_obj.GetDynamicValue(self.default_dynamic_type)
        self.target = self.dynamic_value_obj.GetTarget()

        self.internal_dict = internal_dict
        self.architecture = Helpers.Architecture_unknown
        self.get_architecture()

    def get_architecture(self):
        self.architecture = Helpers.architecture_from_target(self.value_obj.GetTarget())
        return self.architecture

    def is_64bit(self):
        return Helpers.is_64bit_architecture(self.architecture)

    def get_type(self, type_name):
        return TypeCache.get_type_cache().get_type(type_name, self.target)

    @classmethod
    def get_architecture_list(cls):
        if cls._architectures_list is None:
            class_dump_dir = os.path.expanduser(os.path.join(LoadScripts.lldb_scripts_dir,
                                                             LoadScripts.lldb_class_dump_dir))
            cls._architectures_list = ClassDump.LazyArchitecturesList(class_dump_dir)
        return cls._architectures_list

    def summary(self):
        return None
