package main

import (
	"context"
	"encoding/json"
	"io/ioutil"
	"path/filepath"

	pb "github.com/GoogleCloudPlatform/microservices-demo/src/productcatalogservice/genproto"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
)

var tracer = otel.Tracer("productcatalogservice")

// loadCatalog loads the product catalog from local JSON file
func loadCatalog(ctx context.Context) ([]*pb.Product, error) {
	_, span := tracer.Start(ctx, "load-catalog", trace.WithSpanKind(trace.SpanKindInternal))
	defer span.End()

	// Load from local JSON file
	catalogFile := filepath.Join(".", "products.json")
	
	span.SetAttributes(
		attribute.String("catalog.source", "local-file"),
		attribute.String("catalog.file", catalogFile),
	)

	data, err := ioutil.ReadFile(catalogFile)
	if err != nil {
		span.RecordError(err)
		return nil, err
	}

	var catalog struct {
		Products []*pb.Product `json:"products"`
	}

	if err := json.Unmarshal(data, &catalog); err != nil {
		span.RecordError(err)
		return nil, err
	}

	span.SetAttributes(attribute.Int("catalog.product_count", len(catalog.Products)))
	return catalog.Products, nil
}
