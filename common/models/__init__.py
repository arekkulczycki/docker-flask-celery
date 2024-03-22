from logging.config import dictConfig

import yaml

with open("common/logging_config.yml", "rt") as f:
    config = yaml.safe_load(f.read())

dictConfig(config)
