# Python lambda metrics demo
Demo application that sends custom metrics from a python aws lambda function
## The application
The repo contains a simple app written in python:
```python
def handler(event, context):
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
```

## Build and deploy
* create an ecr registry called `python-lambda-metrics-demo`
* Clone this repo
```shell
git clone https://github.com/logzio/python-lambda-metrics-demo.git
```
* Build the image
```shell
docker build . --tag python-lambda-metrics-demo:latest
```
* Authenticate your Docker client to the Amazon ECR registry to which you intend to push your image
```shell
aws ecr get-login-password --region <<region>> | docker login --username AWS --password-stdin <<aws_account_id>>.dkr.ecr.<<region>>.amazonaws.com
```
* If your image repository doesn't exist in the ecr you intend to push to yet, create it.
* Identify the local image to push.
```shell
docker images
```
* Tag your image with the Amazon ECR registry, repository, and optional image tag name combination to use.
```shell
docker tag python-lambda-metrics-demo:latest <<aws_account_id>>.dkr.ecr.<<region>>.amazonaws.com/python-lambda-metrics-demo:latest
```
* Push the image using the docker push command:
```shell
docker push <<aws_account_id>>.dkr.ecr.<<region>>.amazonaws.com/python-lambda-metrics-demo:latest
```
* Go to your lambda console on AWS
* Create a new function from a container image and select the image that you created
* Edit the `LISTENER_URL` (https://listener.logz.io:8053) and `TOKEN` environment variables
* Change the default timout to 30 seconds

