#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import imp

i = imp.find_module(u"mallet", [u".."])
imp.load_module(u"mallet", *i)
import mallet.class_dump as class_dump

if __name__ == "__main__":
    lcdm = class_dump.LazyClassDumpManager()

    current_dir = os.path.abspath(__file__)
    current_dir, _ = os.path.split(current_dir)
    module_path = os.path.join(current_dir, "../mallet/UIKit/class_dumps")
    lcdm.register_module("UIKit", module_path)
    i = lcdm.get_ivar("UIKit", "x86_64", "UINavigationController", "_childViewControllers")
    print(i)

    print(lcdm.modules)
    print(lcdm.modules["UIKit"].architectures)
    print(lcdm.modules["UIKit"].architectures["x86_64"].classes)
