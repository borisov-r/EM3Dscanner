import logging
import EM3Dnalib
import EM3Dreprap


def getValueFromConfig(name, configFile='em3d.conf'):
    # returns value of the name variable
    # in configuration file
    f = open(configFile, 'r')
    # read configuration file
    configuration = f.read()
    # print configuration
    conf = configuration.split()
    i = conf.index(name)
    f.close()
    # real value of name is 2 list items away
    return conf[i + 2]


def main():
    name = getValueFromConfig(name='LOG_FILE_NAME')
    logging.basicConfig(filename=name, level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Started')
    logging.info('LOG_FILE_NAME = %s', name)
    ip = getValueFromConfig(name='PNA_IP_ADDRESS')
    logging.info('PNA_IP_ADDRESS = %s', ip)
    port = getValueFromConfig(name='PNA_PORT')
    logging.info('PNA_PORT = %s', port)

    pna = EM3Dnalib.NetworkAnalyzer()
    logging.info('PNA object added.')
    try:
        pna.connect(IPaddress=ip, Port=port)
        logging.info('PNA ipaddress: %s', pna.IPaddress)
        logging.info('PNA ipaddress: %s', pna.Port)
    except:
        # ? how the exceptions are logged
        logging.exception('Error while connecting to PNA.')

    logging.info('Finished')

if __name__ == '__main__':
    main()
