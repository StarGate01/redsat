import os
import subprocess
import json


def get_location():
    result = subprocess.check_output('source "%s" && echo "{\\"lat\\":$LAT, \\"lon\\":$LON, \\"elv\\":$ELV }"' %\
        os.path.join(os.path.dirname(__file__), "../../persistent-data/config/station.config")
    , shell=True)
    return json.loads(result, encoding='ascii')


if __name__ == "__main__":
    print(get_location())