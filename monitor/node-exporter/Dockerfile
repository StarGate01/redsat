FROM golang as build

# Build container
# Package dependencies

RUN go get github.com/prometheus/node_exporter && \
    cd $GOPATH/src/github.com/prometheus/node_exporter &&\
    make build

# Final Image

FROM alpine:latest

WORKDIR /bin/
COPY --from=build /go/src/github.com/prometheus/node_exporter/node_exporter .

ENTRYPOINT ["/bin/node_exporter"]