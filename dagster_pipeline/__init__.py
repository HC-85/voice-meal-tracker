import logging

from dagster import Definitions

from .assets import all_assets
from .custom_logger import custom_logger

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s @ %(lineno)d: %(message)s")
logging.getLogger("twilio").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

defs = Definitions(assets=all_assets, loggers={"custom": custom_logger})
