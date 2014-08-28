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
import LLDBLogger


class SummaryBase_SynthProvider(object):
    # SummaryBase:

    _architectures_list = None

    def __init__(self, value_obj, internal_dict):
        # self.as_super = super(SummaryBase_SynthProvider, self)
        # self.as_super.__init__()
        super(SummaryBase_SynthProvider, self).__init__()

        self.internal_dict = internal_dict
        self.default_dynamic_type = lldb.eDynamicDontRunTarget
        # self.default_dynamic_type = lldb.eDynamicCanRunTarget

        self.value_obj = value_obj
        self.dynamic_value_obj = self.value_obj.GetDynamicValue(self.default_dynamic_type)
        self.type_name = self.dynamic_value_obj.GetTypeName()
        self.is_pointer_type = self.type_name.endswith("*")
        self.normalized_type_name = self.type_name.rstrip("*").strip()
        self.target = self.dynamic_value_obj.GetTarget()
        self.architecture = Helpers.architecture_type_from_target(self.target)
        self.architecture_name = Helpers.architecture_name_from_target(self.target)
        self.is_64bit = Helpers.is_64bit_architecture(self.architecture)

    def get_type(self, type_name):
        """
        Returns LLDB type from TypeCache.
        """
        return TypeCache.get_type_cache().get_type(type_name, self.target)

    def get_ivar(self, ivar_name):
        """
        Returns Ivar object with given name.
        """
        # LLDBLogger.get_logger().debug("Loading ivar {} for class {} for architecture {}.".
        #                               format(ivar_name, self.normalized_type_name, self.architecture_name))
        return self.get_architecture_list().get_ivar(self.architecture_name, self.normalized_type_name, ivar_name)

    def get_child_value(self, value_name, type_name=None):
        """
        Returns child value (SBValue) with given name. If variable cannot be find by name then uses ivar offset.
        """
        value = self.dynamic_value_obj.GetChildMemberWithName(value_name, self.default_dynamic_type)
        if value:
            # Get dynamic value.
            if not value.IsDynamic():
                value = value.GetDynamicValue(self.default_dynamic_type)
            return value

        # Find ivar and its offset.
        ivar = self.get_ivar(value_name)
        if ivar is None:
            LLDBLogger.get_logger().debug("No ivar {} for class {} for architecture {}.".
                                          format(value_name, self.normalized_type_name, self.architecture_name))
            return None

        # Get value from offset.
        if type_name is None:
            type_name = ivar.ivarType
        value = self.dynamic_value_obj.CreateChildAtOffset(value_name, ivar.offset, self.get_type(type_name))
        # Get dynamic value.
        if value and not value.IsDynamic():
            value = value.GetDynamicValue(self.default_dynamic_type)
        return value

    @classmethod
    def get_architecture_list(cls):
        if cls._architectures_list is None:
            class_dump_dir = os.path.expanduser(os.path.join(LoadScripts.lldb_scripts_dir,
                                                             LoadScripts.lldb_class_dump_dir))
            cls._architectures_list = ClassDump.LazyArchitecturesList(class_dump_dir)
        return cls._architectures_list

    def summary(self):
        return None
