import logging
import logging.config
import yaml


with open('./logging.yaml', 'r') as f_conf:
    dict_conf = yaml.load(f_conf)
logging.config.dictConfig(dict_conf)


logger = logging.getLogger('filelog')

if __name__ == '__main__':
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')