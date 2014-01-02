#! /usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2013 Bartosz Janda
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

import lldb.formatters
import objc_runtime

statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


def generic_SummaryProvider(value_obj, internal_dict, class_synth_provider, supported_classes=[]):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)
    if not class_data.is_valid() or (len(supported_classes) > 0 and class_data.class_name() not in supported_classes):
        return ""
    update_sys_params(value_obj, class_data.sys_params)
    if wrapper is not None:
        return wrapper.message()

    wrapper = class_synth_provider(value_obj, class_data.sys_params, internal_dict)
    if wrapper is not None:
        return wrapper.summary()
    return "Summary Unavailable"


def print_child(value_obj):
    valid = "Valid" if value_obj.IsValid() else "Not valid"
    print "{} {} {}".format(value_obj.GetName(), value_obj.GetAddress(), valid)

    num = value_obj.GetNumChildren()
    for i in xrange(num):
        o = value_obj.GetChildAtIndex(i)
        print "{:<2} - {}".format(i, o.GetName())
        print "{:<2} - {}".format(i, o.GetAddress())
        print "{:<2} - {}".format(i, o.GetType())
        print "{:<2} - {}".format(i, o.GetTypeName())
        print "{:<2} - {}".format(i, o.GetSummary())
        print "{:<2} - {}".format(i, o.GetObjectDescription())
        print ""


def print_child_recursive(value_obj, indent=0):
    indent_str = "  " * indent
    valid = "Valid" if value_obj.IsValid() else "Not valid"
    print "{}{} {} {}".format(indent_str, value_obj.GetName(), value_obj.GetAddress(), valid)
    print "{}{}".format(indent_str, value_obj.GetObjectDescription())

    num = value_obj.GetNumChildren()
    for i in xrange(num):
        o = value_obj.GetChildAtIndex(i)
        print "{}{:<2} - {}".format(indent_str, i, o.GetName())
        print "{}{:<2} - {}".format(indent_str, i, o.GetAddress())
        print "{}{:<2} - {}".format(indent_str, i, o.GetType())
        print "{}{:<2} - {}".format(indent_str, i, o.GetTypeName())
        print "{}{:<2} - {}".format(indent_str, i, o.GetSummary())
        print "{}{:<2} - {}".format(indent_str, i, o.GetObjectDescription())

        n = o.GetNumChildren()
        if n > 0:
            print_child_recursive(o, indent+1)


def update_sys_params(value_obj, sys_params):
    # char, unsigned char
    if not sys_params.types_cache.char:
        sys_params.types_cache.char = value_obj.GetType().GetBasicType(lldb.eBasicTypeChar)
    if not sys_params.types_cache.uchar:
        sys_params.types_cache.uchar = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedChar)

    # short, unsigned short
    if not sys_params.types_cache.short:
        sys_params.types_cache.short = value_obj.GetType().GetBasicType(lldb.eBasicTypeShort)
    if not sys_params.types_cache.ushort:
        sys_params.types_cache.ushort = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedShort)

    # int, unsigned int
    if not sys_params.types_cache.int:
        sys_params.types_cache.int = value_obj.GetType().GetBasicType(lldb.eBasicTypeInt)
    if not sys_params.types_cache.uint:
        sys_params.types_cache.uint = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedInt)

    # long, unsigned long
    if not sys_params.types_cache.long:
        sys_params.types_cache.long = value_obj.GetType().GetBasicType(lldb.eBasicTypeLong)
    if not sys_params.types_cache.ulong:
        sys_params.types_cache.ulong = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedLong)

    # long long, unsigned long long
    if not sys_params.types_cache.longlong:
        sys_params.types_cache.longlong = value_obj.GetType().GetBasicType(lldb.eBasicTypeLongLong)
    if not sys_params.types_cache.ulonglong:
        sys_params.types_cache.ulonglong = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedLongLong)

    # float, double
    if not sys_params.types_cache.float:
        sys_params.types_cache.float = value_obj.GetType().GetBasicType(lldb.eBasicTypeFloat)
    if not sys_params.types_cache.double:
        sys_params.types_cache.double = value_obj.GetType().GetBasicType(lldb.eBasicTypeDouble)

    # NSInteger, NSUInteger
    if not sys_params.types_cache.NSInteger:
        if sys_params.is_64_bit:
            sys_params.types_cache.NSInteger = value_obj.GetType().GetBasicType(lldb.eBasicTypeLong)
        else:
            sys_params.types_cache.NSInteger = value_obj.GetType().GetBasicType(lldb.eBasicTypeInt)
    if not sys_params.types_cache.NSUInteger:
        if sys_params.is_64_bit:
            sys_params.types_cache.NSUInteger = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedLong)
        else:
            sys_params.types_cache.NSUInteger = value_obj.GetType().GetBasicType(lldb.eBasicTypeUnsignedInt)

    # CGFloat
    if not sys_params.types_cache.CGFloat:
        if sys_params.is_64_bit:
            sys_params.types_cache.CGFloat = value_obj.GetType().GetBasicType(lldb.eBasicTypeDouble)
        else:
            sys_params.types_cache.CGFloat = value_obj.GetType().GetBasicType(lldb.eBasicTypeFloat)

    # CGPoint, CGSize, CGRect
    if not sys_params.types_cache.CGPoint:
        sys_params.types_cache.CGPoint = value_obj.GetTarget().FindFirstType('CGPoint')
    if not sys_params.types_cache.CGSize:
        sys_params.types_cache.CGSize = value_obj.GetTarget().FindFirstType('CGSize')
    if not sys_params.types_cache.CGRect:
        sys_params.types_cache.CGRect = value_obj.GetTarget().FindFirstType('CGRect')

    # UIEdgeInsets, UIOffset
    if not sys_params.types_cache.UIEdgeInsets:
        sys_params.types_cache.UIEdgeInsets = value_obj.GetTarget().FindFirstType('UIEdgeInsets')
    if not sys_params.types_cache.UIOffset:
        sys_params.types_cache.UIOffset = value_obj.GetTarget().FindFirstType('UIOffset')

    # id
    if not sys_params.types_cache.id:
        sys_params.types_cache.id = value_obj.GetType().GetBasicType(lldb.eBasicTypeObjCID)

    # NSString, NSAttributedString, NSMutableAttributedString
    if not sys_params.types_cache.NSString:
            sys_params.types_cache.NSString = value_obj.GetTarget().FindFirstType('NSString').GetPointerType()
    if not sys_params.types_cache.NSAttributedString:
        sys_params.types_cache.NSAttributedString = value_obj.GetTarget().FindFirstType('NSAttributedString')\
            .GetPointerType()
    if not sys_params.types_cache.NSMutableAttributedString:
        sys_params.types_cache.NSMutableAttributedString = value_obj.GetTarget()\
            .FindFirstType('NSMutableAttributedString').GetPointerType()

    # NSNumber, NSDecimalNumber
    if not sys_params.types_cache.NSNumber:
        sys_params.types_cache.NSNumber = value_obj.GetTarget().FindFirstType('NSNumber').GetPointerType()
    if not sys_params.types_cache.NSDecimalNumber:
        sys_params.types_cache.NSDecimalNumber = value_obj.GetTarget().FindFirstType('NSDecimalNumber')\
            .GetPointerType()

    # NSURL
    if not sys_params.types_cache.NSURL:
        sys_params.types_cache.NSURL = value_obj.GetTarget().FindFirstType('NSURL').GetPointerType()

    # NSArray, NSSet, NSDictionary
    if not sys_params.types_cache.NSArray:
        sys_params.types_cache.NSArray = value_obj.GetTarget().FindFirstType('NSArray').GetPointerType()
    if not sys_params.types_cache.NSSet:
            sys_params.types_cache.NSSet = value_obj.GetTarget().FindFirstType('NSSet').GetPointerType()
    if not sys_params.types_cache.NSDictionary:
        sys_params.types_cache.NSDictionary = value_obj.GetTarget().FindFirstType('NSDictionary').GetPointerType()


def print_object_info(value_obj):
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)

    print "class_data.cachePointer:                         {:#x}".format(class_data.cachePointer if hasattr(class_data, "cachePointer") else 0x00)
    print "class_data.check_valid():                        {}".format(class_data.check_valid())
    print "class_data.class_name():                         {}".format(class_data.class_name())
    print "class_data.data:                                 {}".format(class_data.data if hasattr(class_data, "data") else None)
    print "class_data.dataPointer:                          {:#x}".format(class_data.dataPointer if hasattr(class_data, "dataPointer") else None)
    print "class_data.get_superclass():                     {}".format(class_data.get_superclass())
    #print "class_data.instance_size():                      {}".format(class_data.instance_size())
    print "class_data.is_cftype():                          {}".format(class_data.is_cftype())
    print "class_data.is_kvo():                             {}".format(class_data.is_kvo())
    print "class_data.is_tagged():                          {}".format(class_data.is_tagged())
    print "class_data.is_valid():                           {}".format(class_data.is_valid())
    print "class_data.isaPointer:                           {:#x}".format(class_data.isaPointer)
    print "class_data.superclassIsaPointer:                 {:#x}".format(class_data.superclassIsaPointer if hasattr(class_data, "superclassIsaPointer") else None) #
    print "class_data.rwt:                                  {}".format(class_data.rwt if hasattr(class_data, "rwt") else None)
    print "class_data.valid:                                {}".format("true" if class_data.valid else "false")
    print "class_data.valobj:                               {}".format(class_data.valobj)

    print ""

    # SystemParameters
    print "class_data.sys_params.cfruntime_size:            {}".format(class_data.sys_params.cfruntime_size)
    print "class_data.sys_params.endianness:                {}".format(class_data.sys_params.endianness)
    print "class_data.sys_params.is_64_bit:                 {}".format(class_data.sys_params.is_64_bit)
    print "class_data.sys_params.is_lion:                   {}".format(class_data.sys_params.is_lion)
    print "class_data.sys_params.is_little:                 {}".format(class_data.sys_params.is_little)
    print "class_data.sys_params.isa_cache:                 {}".format(class_data.sys_params.isa_cache)
    print "class_data.sys_params.pid:                       {}".format(class_data.sys_params.pid)
    print "class_data.sys_params.pointer_size:              {}".format(class_data.sys_params.pointer_size)
    print "class_data.sys_params.runtime_version:           {}".format(class_data.sys_params.runtime_version)
    print "class_data.sys_params.types_cache.addr_type:     {}".format(class_data.sys_params.types_cache.addr_type)
    print "class_data.sys_params.types_cache.addr_ptr_type: {}".format(class_data.sys_params.types_cache.addr_ptr_type)

    if wrapper:
        print dir(wrapper)
