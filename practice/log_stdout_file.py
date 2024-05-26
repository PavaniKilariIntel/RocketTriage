import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler("debug.log",'w'),
        logging.StreamHandler()
    ]
)

logging.info('Useful message')
logging.error('Something bad happened')