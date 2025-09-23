from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, SERVICE_NAME, OTELResourceDetector, Resource


def get_log_handler(*, otlp_service_name: str, otlp_service_instance_id: str) -> LoggingHandler:
    resource = Resource({SERVICE_NAME: otlp_service_name, SERVICE_INSTANCE_ID: otlp_service_instance_id})
    log_provider = LoggerProvider(resource=resource.merge(OTELResourceDetector().detect()))
    log_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))

    return LoggingHandler(logger_provider=log_provider)
