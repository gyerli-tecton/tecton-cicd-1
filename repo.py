from tecton import HiveConfig, BatchSource
from datetime import datetime, timedelta

hive_config = HiveConfig(
    database="gursoy_fraud_simple",
    table="txn",
    timestamp_field="timestamp"
)

txn_batch = BatchSource(
    name="txn_batch",
    batch_config=hive_config,
    owner="gursoy@tecton.ai"
)