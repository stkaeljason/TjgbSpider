#coding: utf-8
# __author__ = jqy

import logging


class Logger(object):
    def __init__(self, log_file):
        """Initialize logging module."""

        # disable requests log
        logging.getLogger("requests").setLevel(logging.DEBUG)

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')

        # Create a file handler to store error messages
        fh = logging.FileHandler(log_file, mode='w')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        # Create a stream handler to print all messages to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        self.logger = logger

    def getLogger(self):
        return self.logger

