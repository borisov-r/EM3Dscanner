"""
This file is using lgging module of python.

In order to have some kind of abstraction I'll define one simple class, which
will open file parascan.log on init and will have 3 functions:
    log.debug( )
    log.info( )
    log.warning( )
"""

import logging


class Log:
    """
    Main class for logging the parascan data.
    On init opens file with 'fileName', when called.
    """
    # create logger with 'logparascan'
    log = logging.getLogger('parascan')
    log.setLevel(logging.DEBUG)

    def __init__(self, fileName):
        # create logger with 'logparascan'
        # self.log = logging.getLogger('logparascan')
        # self.log.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('parascan.log')
        fh.setLevel(logging.DEBUG)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self.log.addHandler(fh)
        self.log.addHandler(ch)
        # set first line of the file
        self.log.info('Initial testing of parascan.py.')
        #self.log.debug('Debug this !')
        print('Log file generated.')

    def debug(self, msg, *args, **kwargs):
        """
        This message will be loged in in to file, when called.
        Message should not contain variables for now !
        -- This should be fixed later on. --
        """
        self.log.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        """
        This message will be loged in in to file, when called.
        Message should not contain variables for now !
        -- This should be fixed later on. --
        """
        self.log.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """
        This message will be loged in in to file, when called.
        Message should not contain variables for now !
        -- This should be fixed later on. --
        """
        self.log.warning(msg, *args, **kwargs)


if __name__ == '__main__':
    log = Log('test.log')
    log.debug('my first DEBUG message %f', 3.14)
    log.info('my first INFO message %f', 3.14576)
    log.warning('my first WARNING message: %s', "Some strings added here.")
