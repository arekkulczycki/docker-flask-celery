from logging.config import dictConfig

import yaml

# Load the config file
with open('logging_config.yml', 'rt') as f:
    config = yaml.safe_load(f.read())

dictConfig(config)
