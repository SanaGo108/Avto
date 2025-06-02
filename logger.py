import logging

def setup_logger():
    logger = logging.getLogger('collateral_calculator')
    handler = logging.FileHandler('logs/parser_log.log')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
