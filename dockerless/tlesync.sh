REDSAT=$(dirname "$(readlink -f "$BASH_SOURCE")")/..
export REDSAT_CONFIG_DIR=${REDSAT}/persistent-data/config
cd ${REDSAT}
./radio/tlesync/run.sh

