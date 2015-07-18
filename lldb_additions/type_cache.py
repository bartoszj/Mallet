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

import helpers
import lldb
import logging


class TypeCache(object):
    """
    Stores cached types.

    :param dict[int, dict[str, lldb.SBType]] targets: Stores cached types per target.
    """
    def __init__(self):
        super(TypeCache, self).__init__()
        self.targets = dict()

    @staticmethod
    def __get_type_from_name(type_name, target):
        """
        Returns type for given name from target (not from cache).

        :param str type_name: Type name.
        :param lldb.SBTarget target: LLDB target.
        :return: Returns SBType for given name.
        :rtype: lldb.SBType | None
        """
        if isinstance(type_name, unicode):
            type_name = type_name.encode('utf-8')
        is_pointer = type_name.endswith("*")
        only_type_name = type_name.rstrip("*").strip()
        t = target.FindFirstType(only_type_name)
        """:type : lldb.SBType"""
        if is_pointer:
            t = t.GetPointerType()

        return t

    @staticmethod
    def __get_target_id(target):
        """
        Returns target process unique id.
        :param lldb.SBTarget target: LLDB target.
        :return: Target process unique id.
        :rtype: int
        """
        process = target.GetProcess()
        """:type: lldb.SBProcess"""
        process_id = process.GetUniqueID()
        """:type: int"""
        return process_id

    def get_type(self, type_name, target):
        """
        Try to find type in cache or ask LLDB to return one.

        :param str type_name: Type name.
        :param lldb.SBTarget target: LLDB target.
        :return: Returns SBType for given name.
        :rtype: lldb.SBType | None
        """
        # Validate data.
        if type_name is None or target is None:
            return None

        target_id = self.__get_target_id(target)
        if target_id not in self.targets:
            self.__populate_standard_types(target, target_id)

        # Find and return type from cache.
        types = self.targets[target_id]
        if type_name in types:
            return types[type_name]

        # Get type from name.
        logger = logging.getLogger(__name__)
        logger.info(u"Adding type \"{}\" to cache.".format(type_name))
        t = self.__get_type_from_name(type_name, target)
        if not t:
            logger.warning(u"Type \"{}\" doesn't exists.".format(type_name))
        types[type_name] = t
        return t

    def clean_cache(self):
        """
        Cleans cached types.
        """
        self.targets = dict()

    def __populate_standard_types(self, target, target_id):
        """
        Populates TypeCache with common LLDB types.

        :param lldb.SBTarget target: LLDB target.
        :param int target_id: Target ID.
        """
        # Do not populate if already data was populated.
        if target_id in self.targets:
            return

        is64bit = helpers.is_64bit_architecture_from_target(target)
        logger = logging.getLogger(__name__)
        logger.debug(u"Populating type cache for target {!r}.".format(target_id))

        # char, unsigned char
        types = dict()
        types["char"] = target.GetBasicType(lldb.eBasicTypeChar)
        types["unsigned char"] = target.GetBasicType(lldb.eBasicTypeUnsignedChar)
        types["short"] = target.GetBasicType(lldb.eBasicTypeShort)
        types["unsigned short"] = target.GetBasicType(lldb.eBasicTypeUnsignedShort)
        types["int"] = target.GetBasicType(lldb.eBasicTypeInt)
        types["unsigned int"] = target.GetBasicType(lldb.eBasicTypeUnsignedInt)
        types["long"] = target.GetBasicType(lldb.eBasicTypeLong)
        types["unsigned long"] = target.GetBasicType(lldb.eBasicTypeUnsignedLong)
        types["long long"] = target.GetBasicType(lldb.eBasicTypeLongLong)
        types["unsigned long long"] = target.GetBasicType(lldb.eBasicTypeUnsignedLongLong)
        types["float"] = target.GetBasicType(lldb.eBasicTypeFloat)
        types["double"] = target.GetBasicType(lldb.eBasicTypeDouble)
        types["uuid_t"] = target.GetBasicType(lldb.eBasicTypeUnsignedInt128)
        types["id"] = target.GetBasicType(lldb.eBasicTypeObjCID)

        if is64bit:
            types["NSInteger"] = target.GetBasicType(lldb.eBasicTypeLong)
            types["NSUInteger"] = target.GetBasicType(lldb.eBasicTypeUnsignedLong)
            types["CGFloat"] = target.GetBasicType(lldb.eBasicTypeDouble)
            types["addr_type"] = target.GetBasicType(lldb.eBasicTypeUnsignedLongLong)
        else:
            types["NSInteger"] = target.GetBasicType(lldb.eBasicTypeInt)
            types["NSUInteger"] = target.GetBasicType(lldb.eBasicTypeUnsignedInt)
            types["CGFloat"] = target.GetBasicType(lldb.eBasicTypeFloat)
            types["addr_type"] = target.GetBasicType(lldb.eBasicTypeUnsignedLong)

        types["addr_ptr_type"] = types["addr_type"].GetPointerType()
        types["void_ptr_type"] = target.GetBasicType(lldb.eBasicTypeVoid).GetPointerType()
        types["CGPoint"] = target.FindFirstType("CGPoint")
        types["CGSize"] = target.FindFirstType("CGSize")
        types["CGRect"] = target.FindFirstType("CGRect")
        types["UIEdgeInsets"] = target.FindFirstType("UIEdgeInsets")
        types["UIOffset"] = target.FindFirstType("UIOffset")
        types["struct CGPoint"] = target.FindFirstType("CGPoint")
        types["struct CGSize"] = target.FindFirstType("CGSize")
        types["struct CGRect"] = target.FindFirstType("CGRect")
        types["struct UIEdgeInsets"] = target.FindFirstType("UIEdgeInsets")
        types["struct UIOffset"] = target.FindFirstType("UIOffset")

        types["NSString *"] = target.FindFirstType("NSString").GetPointerType()
        types["NSAttributedString *"] = target.FindFirstType("NSAttributedString").GetPointerType()
        types["NSMutableAttributedString *"] = target.FindFirstType("NSMutableAttributedString").GetPointerType()
        types["NSNumber *"] = target.FindFirstType("NSNumber").GetPointerType()
        types["NSDecimalNumber *"] = target.FindFirstType("NSDecimalNumber").GetPointerType()
        types["NSURL *"] = target.FindFirstType("NSURL").GetPointerType()
        types["NSDate *"] = target.FindFirstType("NSDate").GetPointerType()
        types["NSData *"] = target.FindFirstType("NSData").GetPointerType()
        types["NSArray *"] = target.FindFirstType("NSArray").GetPointerType()
        types["NSMutableArray *"] = target.FindFirstType("NSMutableArray").GetPointerType()
        types["NSSet *"] = target.FindFirstType("NSSet").GetPointerType()
        types["NSDictionary *"] = target.FindFirstType("NSDictionary").GetPointerType()
        self.targets[target_id] = types


__shared_type_cache = None
""":type: TypeCache"""


def get_type_cache():
    """
    Returns shared TypeCache.

    :return: TypeCache singleton.
    :rtype: TypeCache
    """
    global __shared_type_cache
    if __shared_type_cache is None:
        logger = logging.getLogger(__name__)
        logger.debug(u"Creating shared TypeCache.")
        __shared_type_cache = TypeCache()
    return __shared_type_cache


def clean_type_cache():
    """
    Cleans shared TypeCache.
    """
    global __shared_type_cache
    if __shared_type_cache is not None:
        logger = logging.getLogger(__name__)
        logger.debug(u"Cleaning shared TypeCache.")
        __shared_type_cache.clean_cache()
