from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.metrics import set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, SERVICE_NAME, OTELResourceDetector, Resource


def get_meter_provider(*, otlp_service_name: str, otlp_service_instance_id: str) -> MeterProvider:
    """
    Summary
    -------
    creates and configures a MeterProvider for OpenTelemetry metrics with OTLP exporter

    Parameters
    ----------
    otlp_service_name (str)
        the service name to be used in the OpenTelemetry resource

    otlp_service_instance_id (str)
        the service instance ID to be used in the OpenTelemetry resource

    Returns
    -------
    meter_provider (MeterProvider)
        the configured MeterProvider instance
    """
    system_metrics_config = {
        'process.context_switches': ['involuntary', 'voluntary'],
        'process.cpu.time': ['user', 'system'],
        'process.cpu.utilization': None,
        'process.memory.usage': None,
        'process.memory.virtual': None,
        'process.open_file_descriptor.count': None,
        'process.thread.count': None,
        'process.runtime.memory': ['rss', 'vms'],
        'process.runtime.cpu.time': ['user', 'system'],
        'process.runtime.gc_count': None,
        'cpython.gc.collections': None,
        'cpython.gc.collected_objects': None,
        'cpython.gc.uncollectable_objects': None,
        'process.runtime.thread_count': None,
        'process.runtime.cpu.utilization': None,
        'process.runtime.context_switches': ['involuntary', 'voluntary'],
    }

    resource = Resource({SERVICE_NAME: otlp_service_name, SERVICE_INSTANCE_ID: otlp_service_instance_id})
    merged_resource = resource.merge(OTELResourceDetector().detect())
    meter_provider = MeterProvider([PeriodicExportingMetricReader(OTLPMetricExporter())], merged_resource)
    SystemMetricsInstrumentor(config=system_metrics_config).instrument(meter_provider=meter_provider)
    set_meter_provider(meter_provider)

    return meter_provider
