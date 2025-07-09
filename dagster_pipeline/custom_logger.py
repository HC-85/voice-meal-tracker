from logging import INFO, Logger, getLogger

from dagster import AssetExecutionContext, logger


@logger
def custom_logger(init_context: AssetExecutionContext) -> Logger:
    logger_ = getLogger(__name__)
    logger_.setLevel(INFO)
    return logger_
