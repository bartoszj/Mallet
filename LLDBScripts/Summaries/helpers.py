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


def print_child(valobj):
    valid = "Valid" if valobj.IsValid() else "Not valid"
    print "{} {} {}".format(valobj.GetName(), valobj.GetAddress(), valid)

    num = valobj.GetNumChildren()
    for i in xrange(num):
        o = valobj.GetChildAtIndex(i)
        print "{:<2} - {}".format(i, o.GetName())
        print "{:<2} - {}".format(i, o.GetAddress())
        #print "{:<2} - {}".format(i, o.GetType())
        #print "{:<2} - {}".format(i, o.GetTypeName())
        #print "{:<2} - {}".format(i, o.GetSummary())
        #print "{:<2} - {}".format(i, o.GetObjectDescription())
        print ""


def print_child_recursive(valobj, indent=0):
    indent_str = "  " * indent
    valid = "Valid" if valobj.IsValid() else "Not valid"
    print "{}{} {} {}".format(indent_str, valobj.GetName(), valobj.GetAddress(), valid)
    print "{}{}".format(indent_str, valobj.GetObjectDescription())

    num = valobj.GetNumChildren()
    for i in xrange(num):
        o = valobj.GetChildAtIndex(i)
        print "{}{:<2} - {}".format(indent_str, i, o.GetName())
        print "{}{:<2} - {}".format(indent_str, i, o.GetAddress())
        print "{}{:<2} - {}".format(indent_str, i, o.GetType())
        print "{}{:<2} - {}".format(indent_str, i, o.GetTypeName())
        print "{}{:<2} - {}".format(indent_str, i, o.GetSummary())
        print "{}{:<2} - {}".format(indent_str, i, o.GetObjectDescription())

        n = o.GetNumChildren()
        if n > 0:
            print_child_recursive(o, indent+1)


def get_class_data(valobj):
    global statistics

    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(valobj, statistics)
    return class_data, wrapper


def print_object_info(valobj):
    global statistics
    class_data, wrapper = get_class_data(valobj)

    print "class_data.cachePointer:                         {:#x}".format(class_data.cachePointer)
    print "class_data.check_valid():                        {}".format(class_data.check_valid())
    print "class_data.class_name():                         {}".format(class_data.class_name())
    print "class_data.data:                                 {}".format(class_data.data if hasattr(class_data, "data") else None)
    print "class_data.dataPointer:                          {}".format(class_data.dataPointer if hasattr(class_data, "dataPointer") else None)
    print "class_data.get_superclass():                     {}".format(class_data.get_superclass())
    print "class_data.instance_size():                      {}".format(class_data.instance_size())
    print "class_data.is_cftype():                          {}".format(class_data.is_cftype())
    print "class_data.is_kvo():                             {}".format(class_data.is_kvo())
    print "class_data.is_tagged():                          {}".format(class_data.is_tagged())
    print "class_data.is_valid():                           {}".format(class_data.is_valid())
    print "class_data.isaPointer:                           {:#x}".format(class_data.isaPointer)
    print "class_data.superclassIsaPointer:                 {}".format(class_data.superclassIsaPointer if hasattr(class_data, "superclassIsaPointer") else None) #
    print "class_data.rwt:                                  {}".format(class_data.rwt if hasattr(class_data, "rwt") else None)
    print "class_data.valid:                                {}".format(class_data.valid)
    print "class_data.valobj:                               {}".format(class_data.valobj)
    print "class_data.vtablePointer:                        {:#x}".format(class_data.vtablePointer)

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
    print "class_data.sys_params.types_cache.char:          {}".format(class_data.sys_params.types_cache.char)
    print "class_data.sys_params.types_cache.short:         {}".format(class_data.sys_params.types_cache.short)
    print "class_data.sys_params.types_cache.int:           {}".format(class_data.sys_params.types_cache.int)
    print "class_data.sys_params.types_cache.long:          {}".format(class_data.sys_params.types_cache.long)
    print "class_data.sys_params.types_cache.ulong:         {}".format(class_data.sys_params.types_cache.ulong)
    print "class_data.sys_params.types_cache.longlong:      {}".format(class_data.sys_params.types_cache.longlong)
    print "class_data.sys_params.types_cache.ulonglong:     {}".format(class_data.sys_params.types_cache.ulonglong)
    print "class_data.sys_params.types_cache.uint32_t:      {}".format(class_data.sys_params.types_cache.uint32_t)
    print "class_data.sys_params.types_cache.float:         {}".format(class_data.sys_params.types_cache.float)
    print "class_data.sys_params.types_cache.double:        {}".format(class_data.sys_params.types_cache.double)
    print "class_data.sys_params.types_cache.id:            {}".format(class_data.sys_params.types_cache.id)
    print "class_data.sys_params.types_cache.NSUInteger:    {}".format(class_data.sys_params.types_cache.NSUInteger)
    print "class_data.sys_params.types_cache.NSString:      {}".format(class_data.sys_params.types_cache.NSString)
    print "class_data.sys_params.types_cache.NSNumber:      {}".format(class_data.sys_params.types_cache.NSNumber)

    #print dir(wrapper)
