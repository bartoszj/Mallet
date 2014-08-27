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
import lldb.formatters
import objc_runtime
import LLDBLogger

Architecture_unknown = 0
Architecture_armv7 = 1
Architecture_armv7s = 1
Architecture_arm64 = 2
Architecture_i386 = 3
Architecture_x86_64 = 4


def architecture_from_target(target):
    triple = target.GetTriple()

    architecture = Architecture_unknown
    if triple.startswith("i386"):
        architecture = Architecture_i386
    elif triple.startswith("x86_64"):
        architecture = Architecture_x86_64
    elif triple.startswith("armv7"):
        architecture = Architecture_armv7
    elif triple.startswith("armv7s"):
        architecture = Architecture_armv7s
    elif triple.startswith("arm64"):
        architecture = Architecture_arm64

    return architecture


def is_64bit_architecture(architecture):
    if architecture == Architecture_unknown:
        return False
    if architecture == Architecture_x86_64 or architecture == Architecture_arm64:
        return True
    return False


def is_64bit_architecture_from_target(target):
    architecture = architecture_from_target(target)
    return is_64bit_architecture(architecture)


# Statistics for objc_runtime.
statistics = lldb.formatters.metrics.Metrics()
statistics.add_metric('invalid_isa')
statistics.add_metric('invalid_pointer')
statistics.add_metric('unknown_class')
statistics.add_metric('code_notrun')


def generic_summary_provider(value_obj, internal_dict, class_synthetic_provider, supported_classes=[]):
    # Class data
    global statistics
    class_data, wrapper = objc_runtime.Utilities.prepare_class_detection(value_obj, statistics)

    # Class data invalid.
    if not class_data.is_valid():
        LLDBLogger.get_logger().debug("generic_summary_provider class_data invalid")
        return ""

    # Not supported class.
    if len(supported_classes) > 0 and class_data.class_name() not in supported_classes:
        LLDBLogger.get_logger().debug("generic_summary_provider not supported class")
        return ""

    # Using wrapper if available.
    if wrapper is not None:
        LLDBLogger.get_logger().debug("generic_summary_provider using wrapper")
        return wrapper.message()

    # Using Class Summary Provider.
    wrapper = class_synthetic_provider(value_obj, internal_dict)
    if wrapper is not None:
        # LLDBLogger.get_logger().debug("generic_summary_provider using summary provider")
        return wrapper.summary()

    # Summary not available.
    LLDBLogger.get_logger().debug("generic_summary_provider summary unavailable")
    return "Summary Unavailable"
