from tecton import HiveConfig, BatchSource
from datetime import datetime, timedelta
from tecton import Entity

# A HiveConfig object that points to the table containing the raw data
hive_config = HiveConfig(
    database="gursoy_fraud_simple",
    table="txn",
    timestamp_field="timestamp"
)

# A BatchSource object that points to the Hive table and specifies the owner
txn_batch = BatchSource(
    name="txn_batch",
    batch_config=hive_config,
    owner="gursoy@tecton.ai"
)

from tecton import Entity

user = Entity(
    name='user',
    join_keys=['user_id']
)