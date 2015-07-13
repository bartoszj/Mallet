#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp

i = imp.find_module("lldb_additions", [".."])
imp.load_module("lldb_additions", *i)
import lldb_additions.class_dump as class_dump

if __name__ == "__main__":
    lcdm = class_dump.LazyClassDumpManager()

    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)
    module_path = os.path.join(current_dir, "../lldb_additions/summaries/Foundation/class_dumps")
    lcdm.register_module("NSFoundation", module_path)
    i = lcdm.get_ivar("NSFoundation", "x86_64", "NSLayoutConstraint", "_firstItem")
    print(i)

    print(lcdm.modules)
    print(lcdm.modules["NSFoundation"].architectures)
    print(lcdm.modules["NSFoundation"].architectures["x86_64"].classes)
