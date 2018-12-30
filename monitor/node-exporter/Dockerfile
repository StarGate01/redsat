FROM golang as build

# Build container
# Package dependencies

RUN go get github.com/prometheus/node_exporter && \
    cd $GOPATH/src/github.com/prometheus/node_exporter &&\
    make build

ENTRYPOINT ["/go/src/github.com/prometheus/node_exporter/node_exporter"]