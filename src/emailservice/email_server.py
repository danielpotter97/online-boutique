#!/usr/bin/python

from concurrent import futures
import argparse
import os
import sys
import time
import grpc
import traceback
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateError

import demo_pb2
import demo_pb2_grpc
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc

from opentelemetry import trace
from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

from logger import getJSONLogger
logger = getJSONLogger('emailservice-server')
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('confirmation.html')

class BaseEmailService(demo_pb2_grpc.EmailServiceServicer):
  def Check(self, request, context):
    return health_pb2.HealthCheckResponse(
      status=health_pb2.HealthCheckResponse.SERVING)
  
  def Watch(self, request, context):
    return health_pb2.HealthCheckResponse(
      status=health_pb2.HealthCheckResponse.UNIMPLEMENTED)

class EmailService(BaseEmailService):
  def __init__(self):
    raise Exception('cloud mail client not implemented')
    super().__init__()

  @staticmethod
  def send_email(client, email_address, content):
    response = client.send_message(
      sender = client.sender_path(project_id, region, sender_id),
      envelope_from_authority = '',
      header_from_authority = '',
      envelope_from_address = from_address,
      simple_message = {
        "from": {
          "address_spec": from_address,
        },
        "to": [{
          "address_spec": email_address
        }],
        "subject": "Your Confirmation Email",
        "html_body": content
      }
    )
    logger.info("Message sent: {}".format(response.rfc822_message_id))

  def SendOrderConfirmation(self, request, context):
    email = request.email
    order = request.order

    try:
      confirmation = template.render(order = order)
    except TemplateError as err:
      context.set_details("An error occurred when preparing the confirmation mail.")
      logger.error(err.message)
      context.set_code(grpc.StatusCode.INTERNAL)
      return demo_pb2.Empty()

    try:
      EmailService.send_email(self.client, email, confirmation)
    except Exception as err:
      context.set_details("An error occurred when sending the email.")
      print(str(err))
      context.set_code(grpc.StatusCode.INTERNAL)
      return demo_pb2.Empty()

    return demo_pb2.Empty()

class DummyEmailService(BaseEmailService):
  def SendOrderConfirmation(self, request, context):
    logger.info('A request to send order confirmation email to {} has been received.'.format(request.email))
    return demo_pb2.Empty()

class HealthCheck():
  def Check(self, request, context):
    return health_pb2.HealthCheckResponse(
      status=health_pb2.HealthCheckResponse.SERVING)

def start(dummy_mode):
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10),)
  service = None
  if dummy_mode:
    service = DummyEmailService()
  else:
    raise Exception('non-dummy mode not implemented yet')

  demo_pb2_grpc.add_EmailServiceServicer_to_server(service, server)
  health_pb2_grpc.add_HealthServicer_to_server(service, server)

  port = os.environ.get('PORT', "8080")
  logger.info("listening on port: "+port)
  server.add_insecure_port('[::]:'+port)
  server.start()
  try:
    while True:
      time.sleep(3600)
  except KeyboardInterrupt:
    server.stop(0)

def initJaegerTracing():
  """Initialize OpenTelemetry with Jaeger exporter"""
  jaeger_endpoint = None
  
  try:
    jaeger_endpoint = os.environ.get("JAEGER_ENDPOINT") or os.environ.get("OTEL_EXPORTER_JAEGER_ENDPOINT")
  except KeyError:
    logger.info("Jaeger tracing not configured")
    return

  if jaeger_endpoint:
    try:
      from opentelemetry import trace
      from opentelemetry.exporter.jaeger.thrift import JaegerExporter
      from opentelemetry.sdk.trace import TracerProvider
      from opentelemetry.sdk.trace.export import BatchSpanProcessor
      from opentelemetry.sdk.resources import Resource
      from opentelemetry.semconv.resource import ResourceAttributes
      
      resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: "emailservice",
        ResourceAttributes.SERVICE_VERSION: "1.0.0",
      })
      
      trace.set_tracer_provider(TracerProvider(resource=resource))
      tracer = trace.get_tracer(__name__)
      
      jaeger_exporter = JaegerExporter(
        agent_host_name="jaeger",
        agent_port=6831,
      )
      
      span_processor = BatchSpanProcessor(jaeger_exporter)
      trace.get_tracer_provider().add_span_processor(span_processor)
      
      logger.info("Successfully initialized OpenTelemetry with Jaeger tracing")
      return tracer
    except Exception as exc:
      logger.warning(f"Could not initialize Jaeger tracing: {exc}")
  
  return None


if __name__ == '__main__':
  logger.info('starting the email service in dummy mode.')

  if "DISABLE_PROFILER" not in os.environ:
    logger.info("Platform-independent profiling disabled by default.")
  else:
    logger.info("Profiling disabled.")

  try:
    if os.environ["ENABLE_TRACING"] == "1":
      otel_endpoint = os.getenv("COLLECTOR_SERVICE_ADDR", "localhost:4317")
      trace.set_tracer_provider(TracerProvider())
      trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
            endpoint = otel_endpoint,
            insecure = True
          )
        )
      )
    grpc_server_instrumentor = GrpcInstrumentorServer()
    grpc_server_instrumentor.instrument()

  except (KeyError, DefaultCredentialsError):
      logger.info("Tracing disabled.")
  except Exception as e:
      logger.warn(f"Exception on Cloud Trace setup: {traceback.format_exc()}, tracing disabled.") 
  
  start(dummy_mode = True)
