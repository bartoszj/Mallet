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

import logging
import os


def configure_loggers():
    """
    Configure all well known loggers.
    """

    logger_names = ["lldb_summaries.scripts.class_dump",
                    "lldb_summaries.scripts.helpers",
                    "lldb_summaries.scripts.loader",
                    "lldb_summaries.scripts.logger",
                    "lldb_summaries.scripts.type_cache",
                    "lldb_summaries.summaries.SummaryBase"]
    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)
        configure_logger(logger)


def configure_logger(logger):
    """
    Configure given logger.
    :param logging.Logger logger: Logger object to configure.
    """

    if not hasattr(logger, "LLDB_summaries_configured"):
        logger.LLDB_summaries_configured = True
        logger.setLevel(logging.DEBUG)

        # Formatter.
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)s - %(message)s')

        # File handler.
        file_path = os.path.expanduser("~/Library/Logs/LLDBSummaries.log")
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)

        # Null handler.
        # null_handler = logging.NullHandler()

        logger.addHandler(file_handler)
        # logger.addHandler(null_handler)
        logger.debug("Logger \"{}\" configured.".format(logger.name))


# Configure loggers.
configure_loggers()
