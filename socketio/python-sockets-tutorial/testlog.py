#https://realpython.com/python-logging/

import logging
logging.basicConfig(filename='app.log', level=logging.DEBUG,filemode='w', 
format='%(filename)s,%(funcName)s,%(lineno)d,%(name)s ,%(process)d, %(levelname)s,%(message)s')

#logging.basicConfig(level=logging.INFO)
logging.debug('This will get logged')
logging.info('INFO This will get logged')

