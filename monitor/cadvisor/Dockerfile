FROM golang as build

# Build container
# Package dependencies

RUN go get github.com/google/cadvisor && \
    cd $GOPATH/src/github.com/google/cadvisor &&\
    make build

# Final Image

FROM alpine:latest

WORKDIR /bin/
COPY --from=build src/github.com/google/cadvisor/cadvisor  .

ENTRYPOINT ["/bin/cadvisor"]