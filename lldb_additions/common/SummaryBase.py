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

import lldb
import logging
from .. import loader
from .. import helpers
from .. import type_cache


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
    Base class for all summaries and synthetic child.

    This class adds wrappers around synthetic child for easiest implementation.
    Exists several types of synthetic child wrappers:
    - SYNTHETIC_CHILDREN
      Uses synthetic_children list to present children.

    - SYNTHETIC_PROXY_NAME
      Uses name of registered variable at variable `synthetic_proxy_name` (registered by `register_child_value`)
      to be used as proxy.

    - SYNTHETIC_PROXY_VALUE
      Uses value (lldb.SBValue) at variable `synthetic_proxy_value` to be used as proxy.


    :param dict internal_dict: Internal LLDB dictionary.
    :param int default_dynamic_type: Default dynamic type.
    :param lldb.SBValue value_obj: LLDB variable to compute summary.
    :param lldb.SBValue dynamic_value_obj: Dynamic LLDB variable to compute summary.
    :param str type_name: Type names (used to find ivar in json files).
    :param lldb.SBTarget target: LLDB target (used to manage TypeCache).
    :param int architecture: Architecture type.
    :param str architecture_name: Architecture name.
    :param bool is_64bit: Is 64 bit architecture.
    :param list[RegisterValue] registered_child_values: List of registered parameters.
    :param str synthetic_type: Type of synthetic children (list of proxy object).
    :param list[str] synthetic_children: List of synthetic children.
    :param str synthetic_proxy_name: Name of registered parameter which will be used as proxy for synthetic child.
    :param lldb.SBValue synthetic_proxy_value: LLDB value which will be used as proxy for synthetic child.
    """

    SYNTHETIC_CHILDREN = "SYNTHETIC_CHILDREN"
    SYNTHETIC_PROXY_NAME = "SYNTHETIC_PROXY_NAME"
    SYNTHETIC_PROXY_VALUE = "SYNTHETIC_PROXY_VALUE"

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
        self.module_name = None
        self.type_name = None

        self.target = self.dynamic_value_obj.GetTarget()
        self.architecture = helpers.architecture_type_from_target(self.target)
        self.architecture_name = helpers.architecture_name_from_target(self.target)
        self.is_64bit = helpers.is_64bit_architecture(self.architecture)

        self.registered_child_values = list()
        self.synthetic_type = self.SYNTHETIC_CHILDREN
        self.synthetic_children = list()
        self.synthetic_proxy_name = None
        self.synthetic_proxy_value = None

    def get_type(self, type_name):
        """
        Returns LLDB type from TypeCache.

        :param str type_name: Type name.
        :return: LLDB type from TypeCache.
        :rtype: lldb.SBType | None
        """
        return type_cache.get_type_cache().get_type(type_name, self.target)

    def get_ivar(self, ivar_name):
        """
        Returns Ivar object with given name.

        :param str ivar_name: Ivar name.
        :return: Ivar object with given name.
        :rtype: ClassDump.Ivar | None
        """
        if self.module_name is None:
            logger = logging.getLogger(__name__)
            logger.error("get_ivar: empty module_name.")
            return None
        if self.type_name is None:
            logger = logging.getLogger(__name__)
            logger.error("get_ivar: empty type_name.")
            return None
        return loader.get_shared_lazy_class_dump_manager().get_ivar(self.module_name, self.architecture_name, self.type_name, ivar_name)

    def get_address(self):
        """
        Returns object address.

        :return: Object address.
        :rtype: int
        """
        return get_address_value(self.value_obj)

    def get_child_value(self, ivar_name, type_name=None, offset=None):
        """
        Returns child value (SBValue) with given name (or offset). If variable cannot be find by name then uses ivar offset.

        1. Try to find instance variable using provided offset and type_name.
           If offset is given then type_name also have to be given.
        2. If there is no offset then method try to get child value from LLDB (if possible) using only ivar name.
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

    def num_children(self):
        """
        Synthetic children.
        Return the number of children that the object have.

        :return: Number of children that the object have.
        :rtype: int
        """
        log = logging.getLogger(__name__)
        if self.synthetic_type == self.SYNTHETIC_CHILDREN:
            return len(self.synthetic_children)
        elif self.synthetic_type == self.SYNTHETIC_PROXY_NAME:
            value = getattr(self, self.synthetic_proxy_name)
            """:type: lldb.SBValue"""
            if value is not None:
                value = get_synthetic_value_copy(value)
                count = value.GetNumChildren()
                """:type: int"""
                return count
            log.error("num_children: Cannot get proxy value: {} for type {}.".format(self.synthetic_proxy_name, self.type_name))
            return 0
        elif self.synthetic_type == self.SYNTHETIC_PROXY_VALUE:
            if self.synthetic_proxy_value is not None:
                value = get_synthetic_value_copy(self.synthetic_proxy_value)
                count = value.GetNumChildren()
                """:type: int"""
                return count
            log.error("num_children: No proxy value for type {}.".format(self.type_name))
            # Returns child number for current object.
            return self.value_obj.GetNumChildren()

        log.error("num_children: Unknown synthetic type: {} for type {}.".format(self.synthetic_type, self.type_name))
        return 0

    def get_child_index(self, name):
        """
        Synthetic children.
        Return the index of the synthetic child whose name is given as argument.

        :param str name: Name of synthetic child.
        :return: The index of the synthetic child.
        :rtype: int
        """
        log = logging.getLogger(__name__)
        if self.synthetic_type == self.SYNTHETIC_CHILDREN:
            r = self.get_registered_child_value_parameter(ivar_name=name)
            index = None
            if r is None:
                log.debug("get_child_index: Cannot find registered child with ivar name: {} for class {}.".format(name, self.type_name))
                return index

            if self.synthetic_children.count(r.attribute_name):
                index = self.synthetic_children.index(r.attribute_name)
            else:
                log = logging.getLogger(__name__)
                log.debug("get_child_index: Cannot find child with name: {} for class {}.".format(name, self.type_name))
            return index
        elif self.synthetic_type == self.SYNTHETIC_PROXY_NAME:
            value = getattr(self, self.synthetic_proxy_name)
            """:type: lldb.SBValue"""
            if value is not None:
                value = get_synthetic_value_copy(value)
                index = value.GetIndexOfChildWithName(name)
                """:type: int"""
                return index
            log.error("get_child_index: Cannot get proxy value: {} for type {}.".format(self.synthetic_proxy_name, self.type_name))
            return None
        elif self.synthetic_type == self.SYNTHETIC_PROXY_VALUE:
            if self.synthetic_proxy_value is not None:
                value = get_synthetic_value_copy(self.synthetic_proxy_value)
                index = value.GetIndexOfChildWithName(name)
                """:type: int"""
                return index
            log.error("get_child_index: No proxy value for type {}.".format(self.type_name))
            # Returns index of child for current object.
            return self.value_obj.GetIndexOfChildWithName(name)

        log.error("get_child_index: Unknown synthetic type: {} for type {}.".format(self.synthetic_type, self.type_name))
        return None

    def get_child_at_index(self, index):
        """
        Synthetic children.
        Return a new LLDB SBValue object representing the child at the index given as argument.

        :param int index: Index of synthetic child.
        :return: LLDB SBValue object representing the child.
        :rtype: lldb.SBValue
        """
        log = logging.getLogger(__name__)
        if self.synthetic_type == self.SYNTHETIC_CHILDREN:
            name = self.synthetic_children[index]
            value = getattr(self, name)
            return value
        elif self.synthetic_type == self.SYNTHETIC_PROXY_NAME:
            value = getattr(self, self.synthetic_proxy_name)
            """:type: lldb.SBValue"""
            if value is not None:
                value = get_synthetic_value_copy(value)
                child = value.GetChildAtIndex(index)
                """:type: lldb.SBValue"""
                return child
            log.error("get_child_at_index: Cannot get proxy value: {} for type {}".format(self.synthetic_proxy_name, self.type_name))
            return None
        elif self.synthetic_type == self.SYNTHETIC_PROXY_VALUE:
            if self.synthetic_proxy_value is not None:
                value = get_synthetic_value_copy(self.synthetic_proxy_value)
                child = value.GetChildAtIndex(index)
                """:type: lldb.SBValue"""
                return child
            log.error("get_child_at_index: No proxy value for type {}.".format(self.type_name))
            # Return child for current object.
            return self.value_obj.GetChildAtIndex(index)

        log.error("get_child_at_index: Unknown synthetic type: {} for type {}.".format(self.synthetic_type, self.type_name))
        return None

    def update(self):
        """
        Synthetic children.
        This call should be used to update the internal state of this Python object whenever the state of the variables in LLDB changes.

        This method is optional. Also, it may optionally choose to return a value (starting with SVN rev153061/LLDB-134).
        If it returns a value, and that value is True, LLDB will be allowed to cache the children
        and the children count it previously obtained, and will not return to the provider class to ask.
        If nothing, None, or anything other than True is returned, LLDB will discard the cached information and ask.
        Regardless, whenever necessary LLDB will call update.

        :return: True if internal state of the Python object was changed.
        :rtype: bool
        """
        return True

    def has_children(self):
        """
        Synthetic children.
        This call should return True if this object might have children, and False if this object can be guaranteed not to have children.

        This method is optional (starting with SVN rev166495/LLDB-175). While implementing it in terms of num_children is acceptable,
        implementors are encouraged to look for optimized coding alternatives whenever reasonable.

        :return: True if this object might have children, and False if this object can be guaranteed not to have children.
        :rtype: bool
        """
        log = logging.getLogger(__name__)
        if self.synthetic_type == self.SYNTHETIC_CHILDREN:
            if len(self.synthetic_children) > 0:
                return True
            return True
        elif self.synthetic_type == self.SYNTHETIC_PROXY_NAME:
            value = getattr(self, self.synthetic_proxy_name)
            """:type: lldb.SBValue"""
            if value is not None:
                value = get_synthetic_value_copy(value)
                has_children = value.MightHaveChildren()
                """:type: bool"""
                return has_children
            log.error("has_children: Cannot get proxy value: {} for type {}".format(self.synthetic_proxy_name, self.type_name))
            return True
        elif self.synthetic_type == self.SYNTHETIC_PROXY_VALUE:
            if self.synthetic_proxy_value is not None:
                value = get_synthetic_value_copy(self.synthetic_proxy_value)
                has_children = value.MightHaveChildren()
                """:type: bool"""
                return has_children
            log.error("has_children: No proxy value for type {}.".format(self.type_name))
            # Returns value for current object.
            return self.value_obj.MightHaveChildren()

        log.error("has_children: Unknown synthetic type: {} for type {}.".format(self.synthetic_type, self.type_name))
        return True

    # def get_value(self):
    #     """
    #     Synthetic children.
    #     This call can return an SBValue to be presented as the value of the synthetic value under consideration.
    #
    #     This method is optional (starting with SVN revision 219330). The SBValue you return here will most likely
    #     be a numeric type (int, float, ...) as its value bytes will be used as-if they were the value of the
    #     root SBValue proper. As a shortcut for this, you can inherit from lldb.SBSyntheticValueProvider,
    #     and just define get_value as other methods are defaulted in the superclass as returning default no-children responses.
    #
    #     :return: return an SBValue to be presented as the value of the synthetic value under consideration.
    #     :rtype: lldb.SBValue
    #     """

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

        if self.get_registered_child_value_parameter(attribute_name=attribute_name) is not None:
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

        self.registered_child_values.append(r)

    def get_registered_child_value_parameter(self, attribute_name=None, ivar_name=None):
        """
        Returns registered value parameters for given name or ivar_name.

        :param str attribute_name: Attribute name.
        :param str ivar_name: Ivar name.
        :return: Registered value parameters.
        :rtype: RegisterValue | None
        """
        if attribute_name is not None:
            for r in self.registered_child_values:
                if r.attribute_name == attribute_name:
                    return r
        elif ivar_name is not None:
            for r in self.registered_child_values:
                if r.ivar_name == ivar_name:
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
        # Skipping "builtin" get_value method.
        if item == "get_value":
            return None

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

    def summaries_parts(self):
        """
        Return array of summaries which will be joined in `summary` method.

        :return: Array of summaries
        :rtype: list[str | None]
        """
        return list()

    def summary(self):
        """
        Return object summary.

        :return: Object summary.
        :rtype: str | None
        """
        return join_summaries(*self.summaries_parts())


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
    if obj:
        value = obj.GetValue()
        return None if value is None else float(value)
    return None


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
    Returns stripped summary (without '@"' ot '"' at the beginning and '"' at the end) from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Stripped summary from LLDB value.
    :rtype: str | None
    """
    summary = get_summary_value(obj)

    if summary is None:
        return None

    summary = strip_string(summary)
    return summary


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


def get_stripped_description_value(obj):
    """
    Returns stripped object description (without '@"' ot '"' at the beginning and '"' at the end) from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Object description from LLDB value.
    :rtype: str | None
    """
    description = get_description_value(obj)

    if description is None:
        return None

    description = strip_string(description)
    return description


def get_count_value(obj):
    """
    Returns count of child objects from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Count of child objects from LLDB value.
    :rtype: int | None
    """
    # Passed None value.
    if obj is None:
        return None

    # Return 0 if object has no value.
    if obj.GetValue() is None or obj.GetValueAsUnsigned() == 0:
        return 0
    return obj.GetNumChildren()


def get_synthetic_count_value(obj):
    """
    Returns count of child objects from LLDB synthetic value.

    :param lldb.SBValue obj: LLDB value synthetic object.
    :return: Count of child objects from LLDB synthetic value.
    :rtype: int | None
    """
    # Passed None value.
    if obj is None:
        return None

    # Return 0 if object has no value.
    if obj.GetValue() is None:
        return 0

    # Get synthetic value.
    obj = get_synthetic_value_copy(obj)

    return obj.GetNumChildren()


def get_nsset_count_value(obj):
    """
    Returns count of child objects NSSet using summary value.

    :param lldb.SBValue obj: LLDB value representing NSSet.
    :return: Count of child objects from LLDB synthetic value.
    :rtype: int | None
    """
    summary = get_summary_value(obj)
    if summary is None:
        return None

    values = summary.split(" ")
    if len(values) == 2:
        s = values[0]
        if s.isdigit():
            return int(s)
    return None


def get_address_value(obj):
    """
    Returns address from LLDB value.

    :param lldb.SBValue obj: LLDB value object.
    :return: Address from LLDB value.
    :rtype: int | None
    """
    no_dynamic = obj.GetDynamicValue(lldb.eNoDynamicValues)
    """:type: lldb.SBValue"""
    address = no_dynamic.GetAddress()
    """:type: lldb.SBAddress"""
    address_value = address.GetFileAddress()
    """:type: int"""
    return address_value


def get_type_name_value(obj):
    """
    Returns object type name from LLDB value.

    It returns type name with asterisk if object is a pointer.

    :param lldb.SBValue obj: LLDB value object.
    :return: Object type name from LLDB value.
    :rtype: str | None
    """
    return None if obj is None else obj.GetTypeName()


def get_class_name_value(obj):
    """
    Returns object class name from LLDB value.

    It returns type name without asterisk or ampersand.

    :param lldb.SBValue obj: LLDB value object.
    :return: Object class name from LLDB value.
    :rtype: str | None
    """
    if obj is None:
        return None

    t = obj.GetType()
    """:type: lldb.SBType"""
    if t is None:
        return None

    if t.IsPointerType():
        t = t.GetPointeeType()
    if t.IsReferenceType():
        t = t.GetDereferencedType()

    return None if t is None else t.GetName()


def copy_value(obj):
    """
    Copy SBValue object and preserve dynamic type.

    Useful when `SetPreferDynamicValue()` cannot be used on original object.

    :param lldb.SBValue obj: LLDB object.
    :return: Copy of obj.
    :rtype: lldb.SBValue
    """
    c = obj.GetDynamicValue(obj.GetPreferDynamicValue())
    return c


def get_synthetic_value_copy(obj):
    """
    If object is not synthetic creates new object and set `SetPreferDynamicValue()`.

    :param lldb.SBValue obj: LLDB object.
    :return: Synthetic value.
    :rtype: lldb.SBValue
    """
    if obj.IsSynthetic():
        return obj

    obj = copy_value(obj)
    obj.SetPreferSyntheticValue(True)
    return obj


def strip_string(string):
    # Removes @" or " from the beginning of the string.
    if string.startswith("@\""):
        string = string[2:]
    elif string.startswith("\""):
        string = string[1:]

    # Removes " from the ond of the string.
    if string.endswith("\""):
        string = string[:-1]

    return string


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
    :return: Joined strings.
    :rtype: str | None
    """
    summaries_strings = []
    """:type: list[str]"""
    for summary in args:
        if isinstance(summary, str) and len(summary) > 0:
            summaries_strings.append(summary)

    if len(summaries_strings) == 0:
        return None
    return ", ".join(summaries_strings)
