from datetime import datetime

from dagster import AssetExecutionContext, MaterializeResult, MetadataValue, asset

from extract.extract_vns import extract_voicenotes_from_date
from extract.fetch_msgs import fetch_messages_from_date
from extract.utils import get_twilio_creds

from .partitions import daily_partitions


@asset(partitions_def=daily_partitions, group_name="extraction", kinds=["mongodb", "twilio"])
def daily_messages(context: AssetExecutionContext) -> MaterializeResult:
    partition_date = datetime.strptime(context.partition_key, "%Y-%m-%d")
    fetch_stats = fetch_messages_from_date(get_twilio_creds(), partition_date)
    return MaterializeResult(metadata={k: MetadataValue.int(v) for k, v in fetch_stats.items()})


@asset(
    deps=[daily_messages],
    partitions_def=daily_partitions,
    group_name="extraction",
    kinds=["mongodb", "twilio"],
    # automation_condition=AutomationCondition.eager(),
)
def daily_voicenotes(context: AssetExecutionContext) -> MaterializeResult:
    partition_date = datetime.strptime(context.partition_key, "%Y-%m-%d")
    extract_stats = extract_voicenotes_from_date(partition_date)
    return MaterializeResult(metadata={k: MetadataValue.int(v) for k, v in extract_stats.items()})


@asset(
    deps=[daily_voicenotes],
    partitions_def=daily_partitions,
    group_name="transcription",
    kinds=["mongodb", "postgresql"],
    # automation_condition=AutomationCondition.eager(),
)
def daily_transcriptions(context: AssetExecutionContext) -> MaterializeResult:
    pass


all_assets = [daily_messages, daily_voicenotes]
