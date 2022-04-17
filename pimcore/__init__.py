import os
import logging

class PimApp:
    loglevel = logging.WARNING
    logger = None
    env = None
    modules = {'web', 'cli'}