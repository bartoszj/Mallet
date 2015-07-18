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


class LoggerConfigurator(object):
    """
    Configures logger.
    :param logging.Formatter __formatter: Shared formatter.
    :param logging.FileHandler __file_handler: Shared file handler.
    :param logging.NullHandler __null_handler: Shared NULL handler.
    """
    __HANDLER_NAME = u"lldb_additions_handler"
    __LOGGER_FILE_PATH = os.path.expanduser(u"~/Library/Logs/lldb_additions.log")
    __LOGGER_NAMES = [u"lldb_additions.class_dump",
                      u"lldb_additions.helpers",
                      u"lldb_additions.type_cache",
                      u"lldb_additions.loader",
                      u"lldb_additions.logger",
                      u"lldb_additions.common.SummaryBase",
                      ]

    def __init__(self):
        super(LoggerConfigurator, self).__init__()
        self.__formatter = logging.Formatter(u"%(asctime)s - %(levelname)-8s - %(name)s - %(message)s")
        self.__file_handler = logging.FileHandler(self.__LOGGER_FILE_PATH)
        self.__file_handler.setFormatter(self.__formatter)
        self.__null_handler = logging.NullHandler()

    def __clean_log_file(self):
        """
        Clean log file.
        """
        if os.path.exists(self.__LOGGER_FILE_PATH):
            try:
                with open(self.__LOGGER_FILE_PATH, "w"):
                    pass
            except IOError:
                pass

    def configure_loggers(self):
        """
        Configure all well known loggers.
        """
        self.__clean_log_file()
        for logger_name in self.__LOGGER_NAMES:
            logger = logging.getLogger(logger_name)
            self.__configure_logger(logger)

    def disable_loggers(self):
        """
        Disable all well known loggers.
        """
        self.__clean_log_file()
        for logger_name in self.__LOGGER_NAMES:
            logger = logging.getLogger(logger_name)
            self.__configure_null_logger(logger)

    def __configure_logger(self, logger):
        """
        Configure given logger.

        :param logging.Logger logger: Logger object to configure.
        """
        previous_handler = getattr(logger, self.__HANDLER_NAME, None)
        new_handler = self.__file_handler
        # Remove previous handler and add new only when they are different.
        if previous_handler != new_handler:
            if previous_handler is not None:
                logger.removeHandler(previous_handler)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(new_handler)
            setattr(logger, self.__HANDLER_NAME, new_handler)
            # logger.debug(u"Logger \"{}\" configured.".format(logger.name))

    def __configure_null_logger(self, logger):
        """
        Configure given logger with NullHandler.

        :param logging.Logger logger: Logger object to configure.
        """
        previous_handler = getattr(logger, self.__HANDLER_NAME, None)
        new_handler = self.__null_handler
        # Remove previous handler and add new only when they are different.
        if previous_handler != new_handler:
            if previous_handler is not None:
                logger.removeHandler(previous_handler)
            logger.setLevel(logging.DEBUG)
            logger.addHandler(new_handler)
            setattr(logger, self.__HANDLER_NAME, new_handler)
            # logger.debug(u"Logger \"{}\" configured.".format(logger.name))

__shared_logger_configurator = None
""":type: LoggerConfigurator"""


def get_shared_logger_configurator():
    """
    Returns shared logger configurator.

    :return: Shared logger configurator.
    :rtype: LoggerConfigurator
    """
    global __shared_logger_configurator
    if __shared_logger_configurator is None:
        __shared_logger_configurator = LoggerConfigurator()
    return __shared_logger_configurator
