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
import logging
import ClassDump
import LoadScripts
import Helpers
import TypeCache
import LLDBLogger


class SummaryBase_SynthProvider(object):
    # SummaryBase:
    def __init__(self, value_obj, internal_dict):
        # self.as_super = super(SummaryBase_SynthProvider, self)
        # self.as_super.__init__()
        super(SummaryBase_SynthProvider, self).__init__()

        self.internal_dict = internal_dict
        self.default_dynamic_type = lldb.eDynamicDontRunTarget
        # self.default_dynamic_type = lldb.eDynamicCanRunTarget

        self.value_obj = value_obj
        self.dynamic_value_obj = self.value_obj.GetDynamicValue(self.default_dynamic_type)
        self.type_name = None

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
        if self.type_name is None:
            logger = logging.getLogger(__name__)
            logger.error("get_ivar: empty type_name.")
            return None
        return get_architecture_list().get_ivar(self.architecture_name, self.type_name, ivar_name)

    def get_child_value(self, value_name, type_name=None, offset=None):
        """
        Returns child value (SBValue) with given name (or offset). If variable cannot be find by name then uses ivar offset.
        """
        logger = logging.getLogger(__name__)
        # Using offset if provided.
        if offset is not None:
            if not type_name:
                logger.error("get_child_value: using offset {} without type name."
                             .format(offset))
                return None
            value = self.dynamic_value_obj.CreateChildAtOffset(value_name, offset, self.get_type(type_name))
        # Using name od offset from ivar.
        else:
            value = self.dynamic_value_obj.GetChildMemberWithName(value_name, self.default_dynamic_type)
            if value:
                # Get dynamic value.
                if not value.IsDynamic():
                    value = value.GetDynamicValue(self.default_dynamic_type)
                return value

            # Find ivar and its offset.
            ivar = self.get_ivar(value_name)
            if ivar is None:
                logger.error("get_child_value: no ivar {} for type {}."
                             .format(value_name, self.type_name))
                return None

            # Get value from offset.
            if type_name is None:
                type_name = ivar.ivarType
            value = self.dynamic_value_obj.CreateChildAtOffset(value_name, ivar.offset, self.get_type(type_name))

        # Get dynamic value.
        if value and not value.IsDynamic():
            value = value.GetDynamicValue(self.default_dynamic_type)
        return value

    @staticmethod
    def get_signed_value(obj):
        return None if obj is None else obj.GetValueAsSigned()

    @staticmethod
    def get_unsigned_value(obj):
        return None if obj is None else obj.GetValueAsUnsigned()

    @staticmethod
    def get_float_value(obj):
        return None if obj is None else float(obj.GetValue())

    @staticmethod
    def get_summary_value(obj):
        return None if obj is None else obj.GetSummary()

    @staticmethod
    def get_stripped_summary_value(obj):
        return None if obj is None else obj.GetSummary()[2:-1]

    @staticmethod
    def get_count_value(obj):
        return None if obj is None else obj.GetNumChildren()

    @staticmethod
    def formatted_float(f, precision=2):
        return "{:.{precision}f}".format(f, precision=precision).rstrip("0").rstrip(".")

    def summary(self):
        return None


def get_architecture_list():
    """
    Get shared architecture list.
    """
    if not hasattr(get_architecture_list, "architectures_list"):
        logger = logging.getLogger(__name__)
        logger.debug("Creating shared architecture list.")
        class_dump_dir = os.path.expanduser(os.path.join(LoadScripts.lldb_scripts_dir, LoadScripts.lldb_class_dump_dir))
        get_architecture_list.architectures_list = ClassDump.LazyArchitecturesList(class_dump_dir)
    return get_architecture_list.architectures_list

