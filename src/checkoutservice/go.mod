module github.com/GoogleCloudPlatform/microservices-demo/src/checkoutservice

go 1.23.0

require (
	github.com/google/uuid v1.6.0
	github.com/pkg/errors v0.9.1
	github.com/sirupsen/logrus v1.9.3
	go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc v0.60.0
	go.opentelemetry.io/otel v1.35.0
	go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc v1.35.0
	go.opentelemetry.io/otel/sdk v1.35.0
	google.golang.org/grpc v1.72.2
	google.golang.org/protobuf v1.36.6
)
