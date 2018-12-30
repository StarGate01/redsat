FROM golang as build

# Build container
# Package dependencies

RUN go get github.com/google/cadvisor && \
    cd $GOPATH/src/github.com/google/cadvisor &&\
    make build

ENTRYPOINT ["/go/src/github.com/google/cadvisor/cadvisor"]