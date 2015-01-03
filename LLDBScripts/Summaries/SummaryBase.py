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


class SummaryBaseSyntheticProvider(object):
    """
    Base class for all summaries.

    :param dict internal_dict: Internal LLDB dictionary.
    :param int default_dynamic_type: Default dynamic type.
    :param lldb.SBValue value_obj: LLDB variable to compute summary.
    :param lldb.SBValue dynamic_value_obj: Dynamic LLDB variable to compute summary.
    :param str type_name: Type names (used to find ivar in json files).
    :param lldb.SBTarget target: LLDB target (used to manage TypeCache).
    :param int architecture: Architecture type.
    :param str architecture_name: Architecture name.
    :param bool is_64bit: Is 64 bit architecture.
    """
    def __init__(self, value_obj, internal_dict):
        """
        :param lldb.SBValue value_obj: LLDB variable to compute summary.
        :param dict internal_dict: Internal LLDB dictionary.
        """
        super(SummaryBaseSyntheticProvider, self).__init__()

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

        :param str type_name: Type name.
        :return: LLDB type from TypeCache.
        :rtype: lldb.SBType | None
        """
        return TypeCache.get_type_cache().get_type(type_name, self.target)

    def get_ivar(self, ivar_name):
        """
        Returns Ivar object with given name.

        :param str ivar_name: Ivar name.
        :return: Ivar object with given name.
        :rtype: ClassDump.Ivar | None
        """
        if self.type_name is None:
            logger = logging.getLogger(__name__)
            logger.error("get_ivar: empty type_name.")
            return None
        return get_architecture_list().get_ivar(self.architecture_name, self.type_name, ivar_name)

    def get_child_value(self, value_name, type_name=None, offset=None):
        """
        Returns child value (SBValue) with given name (or offset). If variable cannot be find by name then uses ivar offset.

        1. Try to find instance variable using provided offset and type_name.
           If offset is given then type_name also have to be given.
        2. If there is no offset then method try to get child value from LLDB (if possible) using only name.
        3. If LLDB fails then method try to find offset value (and type name if not provided) from json file.

        :param str value_name: Instance variable name.
        :param str type_name: Type name of ivar.
        :param int offset: Offset value.
        :return: Child value with given name.
        :rtype: lldb.SBValue | None
        """
        logger = logging.getLogger(__name__)
        # Using offset if provided.
        if offset is not None:
            # Error: missing type_name
            if not type_name:
                logger.error("get_child_value: using offset {} without type name.".format(offset))
                return None
            t = self.get_type(type_name)
            # Error: cannot find type with given name.
            if t is None:
                logger.error("get_child_value: cannot find type for name: {}.".format(type_name))
                return None
            value = self.dynamic_value_obj.CreateChildAtOffset(value_name, offset, t)
            """:type: lldb.SBValue"""
        # Using LLDB to get child value
        else:
            value = self.dynamic_value_obj.GetChildMemberWithName(value_name, self.default_dynamic_type)
            """:type: lldb.SBValue"""
            if value:
                # Get dynamic value.
                if not value.IsDynamic():
                    value = value.GetDynamicValue(self.default_dynamic_type)
                    """:type: lldb.SBValue"""
                return value

            # Find ivar object.
            ivar = self.get_ivar(value_name)
            if ivar is None:
                logger.error("get_child_value: no ivar {} for type {}.".format(value_name, self.type_name))
                return None

            # Get value from offset.
            if type_name is None:
                type_name = ivar.ivarType
            t = self.get_type(type_name)

            if t is None:
                logger.error("get_child_value: cannot find type for name: {}.".format(type_name))
                return None
            value = self.dynamic_value_obj.CreateChildAtOffset(value_name, ivar.offset, t)
            """:type: lldb.SBValue"""

        # Get dynamic value.
        if value and not value.IsDynamic():
            value = value.GetDynamicValue(self.default_dynamic_type)
            """:type: lldb.SBValue"""
        return value

    def summary(self):
        """
        Return object summary.

        :return: Object summary.
        :rtype: str | None
        """
        return None


def get_signed_value(obj):
    """
    Returns signed integer from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Signed integer from LLDB value.
    :rtype: int | None
    """
    return None if obj is None else obj.GetValueAsSigned()


def get_unsigned_value(obj):
    """
    Returns unsigned integer from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Unsigned integer from LLDB value.
    :rtype: int | None
    """
    return None if obj is None else obj.GetValueAsUnsigned()


def get_float_value(obj):
    """
    Returns float from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: float from LLDB value.
    :rtype: float | None
    """
    return None if obj is None else float(obj.GetValue())


def get_summary_value(obj):
    """
    Returns summary from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Summary from LLDB value.
    :rtype: str | None
    """
    return None if obj is None else obj.GetSummary()


def get_stripped_summary_value(obj):
    """
    Returns stripped summary (without '@"' at the beginning and '"' at the end) from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Stripped summary from LLDB value.
    :rtype: str | None
    """
    return None if obj is None else obj.GetSummary()[2:-1]


def get_count_value(obj):
    """
    Returns count of child objects from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Count of child objects from LLDB value.
    :rtype: int | None
    """
    return None if obj is None else obj.GetNumChildren()


def formatted_float(f, precision=2):
    """
    Returns formatted float value to given precision (or less).

    :param float f: Float value.
    :return: Formatted float value.
    :rtype: str
    """
    return "{:.{precision}f}".format(f, precision=precision).rstrip("0").rstrip(".")


def get_architecture_list():
    """
    Get shared architecture list.

    :return: Shared architecture list.
    :rtype: ClassDump.LazyArchitecturesList
    """
    if not hasattr(get_architecture_list, "architectures_list"):
        logger = logging.getLogger(__name__)
        logger.debug("Creating shared architecture list.")
        class_dump_dir = os.path.expanduser(os.path.join(LoadScripts.lldb_scripts_dir, LoadScripts.lldb_class_dump_dir))
        get_architecture_list.architectures_list = ClassDump.LazyArchitecturesList(class_dump_dir)
    return get_architecture_list.architectures_list
