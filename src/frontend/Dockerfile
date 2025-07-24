FROM golang:1.23.4-alpine AS builder
ARG TARGETOS
ARG TARGETARCH
WORKDIR /src

# Install git for go mod download
RUN apk add --no-cache git

# restore dependencies
COPY go.mod ./
ENV GOPROXY=https://goproxy.io,direct
RUN go mod download
COPY . .
RUN go mod tidy

# Skaffold passes in debug-oriented compiler flags
ARG SKAFFOLD_GO_GCFLAGS
RUN GOOS=${TARGETOS} GOARCH=${TARGETARCH} CGO_ENABLED=0 go build -gcflags="${SKAFFOLD_GO_GCFLAGS}" -o /go/bin/frontend .

FROM scratch
WORKDIR /src
COPY --from=builder /go/bin/frontend /src/server
COPY ./templates ./templates
COPY ./static ./static

# Definition of this variable is used by 'skaffold debug' to identify a golang binary.
# Default behavior - a failure prints a stack trace for the current goroutine.
# See https://golang.org/pkg/runtime/
ENV GOTRACEBACK=single

EXPOSE 8080
ENTRYPOINT ["/src/server"]
