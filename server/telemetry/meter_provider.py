from collections.abc import Iterable
from os import statvfs
from pathlib import Path

from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.metrics import CallbackOptions, Meter, Observation, set_meter_provider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_INSTANCE_ID, SERVICE_NAME, OTELResourceDetector, Resource


def get_system_filesystem_usage(options: CallbackOptions) -> Iterable[Observation]:  # noqa: ARG001
    with Path("/proc/mounts").open() as mounts:
        mount = next(root_mount for mount in mounts if (root_mount := mount.split())[1] == "/")

    usage = statvfs("/")
    device, mountpoint, filesystem_type, filesystem_mode, *_ = mount
    labels_base = {
        "system.filesystem.device": device,
        "system.filesystem.mountpoint": mountpoint,
        "system.filesystem.type": filesystem_type,
        "system.filesystem.mode": filesystem_mode,
    }

    labels_used = labels_base.copy()
    labels_used["system.filesystem.state"] = "used"
    yield Observation(usage.f_bfree, labels_used)

    labels_free = labels_base.copy()
    labels_free["system.filesystem.state"] = "free"
    yield Observation(usage.f_bavail, labels_free)

    labels_reserved = labels_base.copy()
    labels_reserved["system.filesystem.state"] = "reserved"
    yield Observation(usage.f_bsize * (usage.f_blocks - usage.f_bfree - usage.f_bavail), labels_reserved)


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
        "process.context_switches": ["involuntary", "voluntary"],
        "process.cpu.time": ["user", "system"],
        "process.cpu.utilization": None,
        "process.memory.usage": None,
        "process.memory.virtual": None,
        "process.open_file_descriptor.count": None,
        "process.thread.count": None,
        "process.runtime.memory": ["rss", "vms"],
        "process.runtime.cpu.time": ["user", "system"],
        "process.runtime.gc_count": None,
        "cpython.gc.collections": None,
        "cpython.gc.collected_objects": None,
        "cpython.gc.uncollectable_objects": None,
        "process.runtime.thread_count": None,
        "process.runtime.cpu.utilization": None,
        "process.runtime.context_switches": ["involuntary", "voluntary"],
        "system.filesystem.usage": None,
    }

    resource = Resource({SERVICE_NAME: otlp_service_name, SERVICE_INSTANCE_ID: otlp_service_instance_id})
    merged_resource = resource.merge(OTELResourceDetector().detect())
    meter_provider = MeterProvider([PeriodicExportingMetricReader(OTLPMetricExporter())], merged_resource)
    system_metrics_instrumentor = SystemMetricsInstrumentor(config=system_metrics_config)
    system_metrics_instrumentor.instrument(meter_provider=meter_provider)

    if isinstance(meter := system_metrics_instrumentor._meter, Meter):
        meter.create_observable_up_down_counter(
            "system.filesystem.usage",
            [get_system_filesystem_usage],
            "By",
            "System filesystem usage",
        )

    set_meter_provider(meter_provider)

    return meter_provider
