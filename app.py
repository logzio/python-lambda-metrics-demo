from opentelemetry import metrics
from opentelemetry.exporter.prometheus_remote_write import (
    PrometheusRemoteWriteMetricsExporter,
)
import os
from opentelemetry.sdk.metrics import MeterProvider

import time

# def handler(event, context):
if __name__ == '__main__':

    # configure the Logz.io listener endpoint and Prometheus metrics account token
    exporter = PrometheusRemoteWriteMetricsExporter(
        endpoint=os.environ['LISTENER_URL'] ,
        headers={
            "Authorization": f"Bearer {os.environ['TOKEN']}",
        }
    )
    # set push interval in seconds
    push_interval = 5

    # setup metrics export pipeline
    metrics.set_meter_provider(MeterProvider())
    meter = metrics.get_meter(__name__)
    metrics.get_meter_provider().start_pipeline(meter, exporter, push_interval)

    # create a counter instrument and provide the first data point
    counter = meter.create_counter(
        name="MyCounter",
        description="Description of MyCounter",
        unit="1",
        value_type=int
    )
    # add labels
    labels = {
        "service.name": "service123",
        "service.version": "1.2.3"
    }
    counter.add(25, labels)
    metrics.get_meter_provider().shutdown()

