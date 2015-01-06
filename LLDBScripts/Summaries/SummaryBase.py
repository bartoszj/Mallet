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


class RegisterValue(object):
    """
    Stores register value parameters.

    :param str attribute_name: Child value name.
    :param str ivar_name: Instance variable name.
    :param str type_name: Type name of child value.
    :param int offset: Offset of child value.
    :param bool cache_value: Indicates if child value should be cached.
    :param lldb.SBValue cached_value: Cached child value.
    :param (lldb.SBValue | (SummaryBaseSyntheticProvider | lldb.SBValue)) -> int | float | str | None primitive_value_function: Function that return primitive vale of object.
    :param bool cache_primitive_value: Indicates if primitive value should be cached.
    :param int | float | str | None cached_primitive_value: Cached primitive value.
    :param class provider_class: Provider class (subclass of SummaryBase).
    :param bool cache_provider: Indicates if provider should be cached.
    :param SummaryBaseSyntheticProvider cached_provider: Cached provider.
    :param (int | float | str | SummaryBaseSyntheticProvider) -> str | None summary_function: Summary function.
    :param bool cache_summary: Indicates if summary value should be cached.
    :param str | None cached_summary: Cached summary.
    """
    def __init__(self):
        self.attribute_name = None
        self.ivar_name = None
        self.type_name = None
        self.offset = None
        self.cache_value = True
        self.cached_value = None

        self.primitive_value_function = None
        self.cache_primitive_value = False
        self.cached_primitive_value = None

        self.provider_class = None
        self.cache_provider = None
        self.cached_provider = None

        self.summary_function = None
        self.cache_summary = False
        self.cached_summary = None


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
    :param list[RegisterValue] registeredChildValues: List of registered parameters.
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

        self.registeredChildValues = list()

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

    def get_child_value(self, ivar_name, type_name=None, offset=None):
        """
        Returns child value (SBValue) with given name (or offset). If variable cannot be find by name then uses ivar offset.

        1. Try to find instance variable using provided offset and type_name.
           If offset is given then type_name also have to be given.
        2. If there is no offset then method try to get child value from LLDB (if possible) using only name.
        3. If LLDB fails then method try to find offset value (and type name if not provided) from json file.

        :param str ivar_name: Instance variable name.
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
            value = self.dynamic_value_obj.CreateChildAtOffset(ivar_name, offset, t)
            """:type: lldb.SBValue"""
        # Using LLDB to get child value
        else:
            value = self.dynamic_value_obj.GetChildMemberWithName(ivar_name, self.default_dynamic_type)
            """:type: lldb.SBValue"""
            if value:
                # Get dynamic value.
                if not value.IsDynamic():
                    value = value.GetDynamicValue(self.default_dynamic_type)
                    """:type: lldb.SBValue"""
                return value

            # Find ivar object.
            ivar = self.get_ivar(ivar_name)
            if ivar is None:
                logger.error("get_child_value: no ivar {} for type {}.".format(ivar_name, self.type_name))
                return None

            # Get value from offset.
            if type_name is None:
                type_name = ivar.ivarType
            t = self.get_type(type_name)

            if t is None:
                logger.error("get_child_value: cannot find type for name: {}.".format(type_name))
                return None
            value = self.dynamic_value_obj.CreateChildAtOffset(ivar_name, ivar.offset, t)
            """:type: lldb.SBValue"""

        # Get dynamic value.
        if value and not value.IsDynamic():
            value = value.GetDynamicValue(self.default_dynamic_type)
            """:type: lldb.SBValue"""
        return value

    def register_child_value(self, attribute_name, ivar_name=None, type_name=None, offset=None, cache_value=True,
                             primitive_value_function=None, cache_primitive_value=False,
                             provider_class=None, cache_provider=True,
                             summary_function=None, cache_summary=False):
        """
        Creates four attributes:
        1. `attribute_name` - Stores child value object (SBValue) using ivar_name, type_name and offset.
        2. `attribute_name`_value - Stores primitive value of object, like integer, string.
        3. `attribute_name`_provider - Stores object provider.
        4. `attribute_name`_summary - Stores child value summary based on summary_format.

        if both primitive_value_function and provider_class are specified, then primitive_value_function is used.
        If both primitive_value_function and provider_class are None, then `attribute_name`_summary will raise exception.
        If summary_function is None then `attribute_name`_summary will raise exception.

        :param str attribute_name: Child value name.
        :param str ivar_name: Instance variable name.
        :param str type_name: Type name of child value.
        :param int offset: Offset of child value.
        :param bool cache_value: Indicates if child value should be cached.
        :param (lldb.SBValue | (SummaryBaseSyntheticProvider | lldb.SBValue)) -> int | float | str | None primitive_value_function: Function or method
        that returns primitive vale of object.
        :param bool cache_primitive_value: Indicates if primitive value should be cached.
        :param class provider_class: Provider class (subclass of SummaryBaseSyntheticProvider).
        :param bool cache_provider: Indicates if provider should be cached.
        :param (int | float | str | SummaryBaseSyntheticProvider) -> str | None summary_function: Summary function or method.
        Summary function will be called only when primitive value or provider is not None.
        :param bool cache_summary: Indicates if summary value should be cached.
        """

        if self.get_registered_child_value_parameter(attribute_name) is not None:
            # Registered value already exists.
            raise StandardError("Attribute \"{}\" already registered.".format(attribute_name))

        # Create registered child value parameters.
        r = RegisterValue()

        # Child value.
        r.attribute_name = attribute_name
        r.ivar_name = ivar_name
        r.type_name = type_name
        r.offset = offset
        r.cache_value = cache_value

        # Primitive value.
        r.primitive_value_function = primitive_value_function
        r.cache_primitive_value = cache_primitive_value

        # Provider.
        r.provider_class = provider_class
        r.cache_provider = cache_provider

        # Summary value.
        r.summary_function = summary_function
        r.cache_summary = cache_summary

        self.registeredChildValues.append(r)

    def get_registered_child_value_parameter(self, attribute_name):
        """
        Returns registered value parameters for given name.

        :param str attribute_name: Attribute name.
        :return: Registered value parameters.
        :rtype: RegisterValue
        """
        for r in self.registeredChildValues:
            if r.attribute_name == attribute_name:
                return r
        return None

    def __getattr__(self, item):
        """
        Returns computed values of registered child values.

        :param str item: Attribute name.
        :return: Computed values of registered child values.
        :rtype: lldb.SBValue | str | int | float | None
        :raises AttributeError: If registered attribute doesn't exists.
        """
        logger = logging.getLogger(__name__)
        # Check is child value, primitive value or summary value should be returned.
        attribute_name = item
        primitive_value = False
        provider_value = False
        summary_value = False
        if item.endswith("_value"):
            index = item.rfind("_value")
            primitive_value = True
            attribute_name = item[:index]
        elif item.endswith("_provider"):
            index = item.rfind("_provider")
            provider_value = True
            attribute_name = item[:index]
        elif item.endswith("_summary"):
            index = item.rfind("_summary")
            summary_value = True
            attribute_name = item[:index]

        # Get registered value.
        r = self.get_registered_child_value_parameter(attribute_name)
        if r is None:
            logger.error("__getattr__: Cannot find registered attribute \"{}\" in object {}.".format(attribute_name, self.type_name))
            raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, attribute_name))

        # Get child value.
        if primitive_value is False and provider_value is False and summary_value is False:
            # logger.debug("__getattr__: Getting child value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            # Get cached value.
            if r.cache_value is True and r.cached_value is not None:
                # logger.debug("__getattr__: Getting cached child value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return r.cached_value

            # Computing child value.
            # logger.debug("__getattr__: Computing child value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            value = self.get_child_value(r.ivar_name, r.type_name, r.offset)
            if r.cache_value is True:
                r.cached_value = value
            return value
        # Getting primitive value.
        elif primitive_value is True:
            # logger.debug("__getattr__: Getting primitive value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            # Check is primitive function exists.
            if r.primitive_value_function is None:
                logger.error("__getattr__: Primitive function not found for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, item))

            # Get cached value.
            if r.cache_primitive_value is True and r.cached_primitive_value is not None:
                # logger.debug("__getattr__: Getting cached primitive value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return r.cached_primitive_value

            # Get child value.
            # logger.debug("__getattr__: Computing primitive value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            value = getattr(self, attribute_name)
            """:type: lldb.SBValue"""
            if value is None:
                # logger.debug("__getattr__: Cannot compute child value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return None

            # Computing primitive value.
            primitive = r.primitive_value_function(value)
            if r.cache_primitive_value is True:
                r.cached_primitive_value = primitive
            return primitive
        # Getting provider.
        elif provider_value is True:
            # logger.debug("__getattr__: Getting provider for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            # Check is provider class exists.
            if r.provider_class is None:
                logger.error("__getattr__: Provider class not found for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, item))

            # Get cached value.
            if r.cache_provider is True and r.cached_provider is not None:
                # logger.debug("__getattr__: Getting cached provider for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return r.cached_provider

            # Get child value.
            # logger.debug("__getattr__: Computing provider for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            value = getattr(self, attribute_name)
            """:type: lldb.SBValue"""
            if value is None:
                # logger.debug("__getattr__: Cannot compute child value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return None

            # Computing provider.
            provider = r.provider_class(value, self.internal_dict)
            """:type: SummaryBaseSyntheticProvider"""
            if r.cache_provider is True:
                r.cached_provider = provider
            return provider
        # Getting summary.
        elif summary_value is True:
            # logger.debug("__getattr__: Getting summary for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            # Check if summary function exists.
            if r.summary_function is None:
                logger.error("__getattr__: Summary function not found for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, item))

            # Check if primitive function and provider class are None.
            if r.primitive_value_function is None and r.provider_class is None:
                logger.error("__getattr__: Primitive function and provider class not found for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                raise AttributeError("{!r} object has no attribute {!r}".format(self.__class__, item))

            # Get cached summary.
            if r.cache_summary is True and r.cached_summary is not None:
                # logger.debug("__getattr__: Getting cached summary for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                return r.cached_summary

            # Getting primitive value.
            # logger.debug("__getattr__: Computing summary for name \"{}\" in object {}.".format(attribute_name, self.type_name))
            if r.primitive_value_function:
                primitive = getattr(self, attribute_name+"_value")
                """:type: str | int | float | None"""
                if primitive is None:
                    # logger.debug("__getattr__: Cannot compute primitive value for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                    return None
                summary_function_parameter = primitive
            else:
                provider = getattr(self, attribute_name+"_provider")
                """:type: SummaryBaseSyntheticProvider"""
                if provider is None:
                    # logger.debug("__getattr__: Cannot compute provider for name \"{}\" in object {}.".format(attribute_name, self.type_name))
                    return None
                summary_function_parameter = provider

            # Computing summary.
            summary = r.summary_function(summary_function_parameter)
            if r.cache_summary is True:
                r.cached_summary = summary
            return summary

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


def get_bool_value(obj):
    """
    Returns bool from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Bool from LLDB value.
    :rtype: bool | None
    """
    value = get_signed_value(obj)
    if value is None:
        return None
    if value == 0:
        return False
    return True


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
    summary = get_summary_value(obj)
    return None if summary is None else summary[2:-1]


def get_description_value(obj):
    """
    Returns object description from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Object description from LLDB value.
    :rtype: str | None
    """
    desc = None if obj is None else obj.GetObjectDescription()
    if desc == "<nil>":
        desc = None
    return desc


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


def join_summaries(*args):
    """
    Joins summaries. If summary value is not string, it will be ignored.

    :param str separator: Summary separator.
    :param list[str] args: List of summaries.
    :return:
    """
    summaries_strings = []
    """:type: list[str]"""
    for summary in args:
        if isinstance(summary, str):
            summaries_strings.append(summary)

    return ", ".join(summaries_strings)


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
