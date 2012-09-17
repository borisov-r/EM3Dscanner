r"""ErrorMessage module.

This class is part of 3DEMscanner suit.

Example:

>>> ErrorMessage.fromInit.show()
>>> ErrorMessage.fromReprap.show()
>>> ErrorMessage.fromPNA.show()

ErrorMessage class is the main class for three subclases:

    fromInit
    fromReprap
    fromPNA

To do:
    -
    -
    -

"""

import logging


class ErrorMessage:

    """ErrorMessage interface class.

    An instace of this class represnts a data that can be stored and shown
    when an error ocures in 3DEMscanner program suit.

    This class will be more general that the three other classes, which
    will contain the methods to add, change and remove messages.

    """

    pass

logging.warning('Watch out!')  # will print a message to the console
logging.info('I told you so')  # will not print anything

logging.basicConfig(filename='example.log', level=logging.DEBUG)
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
