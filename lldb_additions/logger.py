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

__logger_file_path = os.path.expanduser("~/Library/Logs/lldb_additions.log")


def __clean_log_file():
    if os.path.exists(__logger_file_path):
        try:
            with open(__logger_file_path, "w") as f:
                pass
        except IOError:
            pass


def configure_loggers():
    """
    Configure all well known loggers.
    """
    logger_names = ["lldb_additions.class_dump",
                    "lldb_additions.helpers",
                    "lldb_additions.type_cache",
                    "lldb_additions.loader",
                    "lldb_additions.logger",
                    "lldb_additions.common.SummaryBase",
                    ]
    for logger_name in logger_names:
        logger = logging.getLogger(logger_name)
        # configure_null_logger(logger)
        configure_logger(logger)


def configure_null_logger(logger):
    """
    Configure given logger with NullHandler.

    :param logging.Logger logger: Logger object to configure.
    """
    # Remove previous file handle if it is not a NullHandler.
    if hasattr(logger, "lldb_additions_handler"):
        handler = logger.lldb_additions_handler
        """:type: logging.Handler"""
        if isinstance(handler, logging.NullHandler) is False:
            logger.removeHandler(handler)
            del logger.lldb_additions_handler

    # Add FileHandler.
    if not hasattr(logger, "lldb_additions_handler"):
        logger.lldb_additions_logger = True
        logger.setLevel(logging.DEBUG)

        # Null handler.
        null_handler = logging.NullHandler()

        logger.addHandler(null_handler)
        logger.lldb_additions_logger = null_handler


def configure_logger(logger):
    """
    Configure given logger.
    :param logging.Logger logger: Logger object to configure.
    """
    # Remove previous file handle if it is not a FileHandler.
    if hasattr(logger, "lldb_additions_handler"):
        handler = logger.lldb_additions_handler
        """:type: logging.Handler"""
        if isinstance(handler, logging.FileHandler) is False:
            logger.removeHandler(handler)
            del logger.lldb_additions_handler

    # Add FileHandler.
    if not hasattr(logger, "lldb_additions_handler"):
        logger.setLevel(logging.DEBUG)

        # Formatter.
        formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(name)s - %(message)s')

        # File handler.
        file_path = __logger_file_path
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.lldb_additions_handler = file_handler
        # logger.debug("Logger \"{}\" configured.".format(logger.name))


# Configure loggers.
__clean_log_file()
configure_loggers()
