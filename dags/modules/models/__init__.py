import logging
import os

TABLE_PREFIX_ENV_VAR = "TABLE_PREFIX"
TABLE_PREFIX = os.get(TABLE_PREFIX_ENV_VAR)
if not TABLE_PREFIX:
    raise RuntimeError("env variable 'TABLE_PREFIX_ENV_VAR' not found")
else:
    logging.debug("found env variable for table_prefix: %s", TABLE_PREFIX)
