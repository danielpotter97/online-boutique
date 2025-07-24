FROM golang:1.23.4-alpine AS builder
ARG TARGETOS
ARG TARGETARCH
WORKDIR /src

RUN apk add --no-cache git

COPY go.mod ./
RUN go mod download
COPY . .
RUN go mod tidy

ARG SKAFFOLD_GO_GCFLAGS
RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} CGO_ENABLED=0 go build -gcflags="${SKAFFOLD_GO_GCFLAGS}" -o /go/bin/shippingservice .

FROM scratch

WORKDIR /src
COPY --from=builder /go/bin/shippingservice /src/shippingservice
ENV APP_PORT=50051

# Definition of this variable is used by 'skaffold debug' to identify a golang binary.
# Default behavior - a failure prints a stack trace for the current goroutine.
# See https://golang.org/pkg/runtime/
ENV GOTRACEBACK=single

EXPOSE 50051
ENTRYPOINT ["/src/shippingservice"]
