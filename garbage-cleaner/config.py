import logging
import yaml
import os


def read_config() -> dict:
    with open(os.path.join("garbage-cleaner", "config.yaml")) as stream:
        return yaml.safe_load(stream)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s:%(message)s",
)

config = read_config()
host = config["host"]
admin_username = config["admin_username"]
admin_password = config["admin_password"]
entity_min_age = config["entity_min_age"]
