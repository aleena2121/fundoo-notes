import json
import os

from loguru import logger


class Logger:

    @staticmethod
    def initialize_from_json(config_path="logger_config.json"):
        logger.remove()
        
        def db_filter(record):
            return record.get("extra", {}).get("db", False)
        
        def func_filter(record):
            return record.get("extra", {}).get("func", False)

        abs_path = os.path.join(os.path.dirname(__file__), config_path)
        with open(abs_path, 'r') as f:
            config = json.load(f)

        for handler in config["handlers"]:
            filter_name = handler.pop("filter", None)
            filter_func = {"db": db_filter,"func": func_filter}.get(filter_name)
            
            logger.add(**handler, filter=filter_func)

        logger.info("Logger initialized from JSON config.")
        return logger