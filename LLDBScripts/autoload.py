#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

lldb_auto_load_paths = ["~/Library/LLDBScripts/Commands",
                        "~/Library/LLDBScripts/Summaries"]
lldb_script_endings = [".py"]


def __lldb_init_module(debugger, dict):
    # Go through all files
    to_load = set()
    endings = tuple(lldb_script_endings)

    # Go through all lldb auto load paths
    for path in lldb_auto_load_paths:
        # Got through all folders in auto load paths
        for root, dirs, files in os.walk(os.path.expanduser(path)):
            # Got through all files
            for f in files:
                # Add only files with correct endings
                if f.endswith(endings):
                    full_file_path = os.path.join(root, f)
                    to_load.add(full_file_path)
                    #print full_file_path

    # Load all scripts
    for script_path in to_load:
        command = "command script import \"{}\"".format(script_path)
        debugger.HandleCommand(command)
        #print script_path
        #print command
