import os
import logging

class PimApp:
    loglevel = logging.WARNING
    logger = None
    env = None
    modules = {'web', 'cli', 'maintenance'}
    config = None

    def __init__(self, config):
        self.config = config
