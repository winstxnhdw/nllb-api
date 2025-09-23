from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, SERVICE_NAME, OTELResourceDetector, Resource


def get_meter_provider(*, otlp_service_name: str, otlp_service_instance_id: str) -> MeterProvider:
    resource = Resource({SERVICE_NAME: otlp_service_name, SERVICE_INSTANCE_ID: otlp_service_instance_id})
    merged_resource = resource.merge(OTELResourceDetector().detect())
    meter_provider = MeterProvider([PeriodicExportingMetricReader(OTLPMetricExporter())], merged_resource)
    set_meter_provider(meter_provider)

    return meter_provider
