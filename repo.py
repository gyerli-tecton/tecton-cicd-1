from tecton import HiveConfig, BatchSource
from datetime import datetime, timedelta
from tecton import Entity
from tecton import (
    FeatureView,
    FilteredSource,
    Aggregation,
    materialization_context,
    batch_feature_view)

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

user = Entity(
    name='user',
    join_keys=['user_id']
)

# A FeatureView that ingests data from the BatchSource defined above
@batch_feature_view(
    name="user_txns_custom_7d",
    sources=[FilteredSource(txn_batch, start_time_offset=timedelta(days=-6))],
    entities=[user],
    mode="spark_sql",
    online=True,
    offline=True,
    batch_schedule=timedelta(days=1),
    ttl=timedelta(days=1),
    feature_start_time=datetime(2023, 8, 10),
    incremental_backfills=True
)
def user_txns_custom_7d(txn_batch, context=materialization_context()):
    return f"""
        select
            user_id,
            to_timestamp("{context.end_time}") - interval 1 microsecond as timestamp,
            count(user_id) as cnt
        from
            {txn_batch}
        group by user_id
        """
