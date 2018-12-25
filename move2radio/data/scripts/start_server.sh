(nc -l -u 12345 | socat - TCP-LISTEN:1234,fork,reuseaddr) &
