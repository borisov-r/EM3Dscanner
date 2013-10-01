import logging


class LogData(object):
    ''' Creates log file, where every log message is appended
    '''
    def __init__(self, level, name='em3d.log'):
        # start logging in 'em3d.log' file
        self.name = name
        self.level = level
        logging.basicConfig(filename=name,
                            level=self.level, filemode='w',
                            format='%(asctime)s %(levelname)s %(message)s')
        self.append("Logging started")

    def append(self, message):
        # append to log file
        if self.level == 10:
            logging.debug(message)
        #
        # logging.INFO
        elif self.level == 20:
            logging.info(message)
        #
        # logging.WARNING
        elif self.level == 30:
            logging.warning(message)
        #
        # logging.ERROR
        elif self.level == 40:
            logging.error(message)
        #
        # logging.CRITICAL
        elif self.level == 50:
            logging.critical(message)
        #
        else:
            pass

    def warn(self, message):
        # print something to console
        logging.warning(message)


def main():
    log = LogData(20)
    log.append("Logging finished")

if __name__ == '__main__':
    main()
