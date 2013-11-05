#! /usr/bin/env python
# -*- coding: utf-8 -*-

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
        print "{:<2} - {}".format(i, o.GetType())
        print "{:<2} - {}".format(i, o.GetTypeName())
        print "{:<2} - {}".format(i, o.GetSummary())
        print "{:<2} - {}".format(i, o.GetObjectDescription())
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


def print_object_info(valobj):
    global statistics

    #print_child_recursive(valobj)
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(valobj, statistics)
    print "class_data.cachePointer:                         {}".format(class_data.cachePointer)
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
    print "class_data.isaPointer:                           {}".format(class_data.isaPointer)
    print "class_data.superclassIsaPointer:                 {}".format(class_data.superclassIsaPointer if hasattr(class_data, "superclassIsaPointer") else None) #

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
    print "class_data.sys_params.types_cache.long:          {}".format(class_data.sys_params.types_cache.long)
    print "class_data.sys_params.types_cache.uint32_t:      {}".format(class_data.sys_params.types_cache.uint32_t)

    print "class_data.rwt:                                  {}".format(class_data.rwt if hasattr(class_data, "rwt") else None)
    print "class_data.valid:                                {}".format(class_data.valid)
    print "class_data.valobj:                               {}".format(class_data.valobj)
    print "class_data.vtablePointer:                        {}".format(class_data.vtablePointer)

    #print dir(wrapper)
