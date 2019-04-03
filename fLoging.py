import logging
import logging.handlers
import datetime


class fortressLogger():
    init_logger = logging.getLogger('fortress')
    init_logger.setLevel(logging.DEBUG)

    log_time_tag = datetime.datetime.strftime(datetime.date.today(),'%Y%m%d')


    # logger.extra = extra_dict
    rf_handler = logging.handlers.TimedRotatingFileHandler('logs/fortress_%s.log'%log_time_tag, when='midnight', interval=1, backupCount=7, atTime=datetime.time(0, 0, 0, 0))
    rf_handler.setFormatter(logging.Formatter("{\"time\":\"%(asctime)s\",\"level\":\"%(levelname)s\",\"client_ip\":\"%(ip)s\",\"sport\":\"%(sport)s\",\"dport\":\"%(dport)s\",\"ssh_tty\":\"%(ssh_tty)s\",\"user\":\"%(username)s\" \"detail\":\"%(message)s\"}"))
    extra_dict = {"client_ip": "IP", "username": "USERNAME",'sport':'sport','dport':'dport','ssh_tty':'ssh_tty'}

    init_logger.addHandler(rf_handler)
    logger = logging.LoggerAdapter(init_logger,extra_dict)

    @classmethod
    def flogger(cls):
        return cls.logger


if __name__ == '__main__':
    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warning message')
    # logger.extra = {"ip": "113.208.78.29", "username": "Petter"}
    # logger.error('error message')
    # logger.critical('critical message')
    l = fortressLogger.flogger()

    l.extra = {"ip": "113.208.78.29", "username": "Petter"}
    l.error('error')