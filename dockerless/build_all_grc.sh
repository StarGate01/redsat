REDSAT=$(dirname "$(readlink -f "$BASH_SOURCE")")/..
cd ${REDSAT}/radio

SRC_COMMON=(common/data/gr/doppler_correction.grc common/data/gr/range_selector.grc common/data/gr/file_source.grc)

SRC=("${SRC_COMMON[@]}" $(find . -type f -name "*.grc" | tr '\n' ' '))

# TODO don't compile the common files twice
for file in ${SRC[@]}
do
	echo "Building $file"
	grcc $file
done
