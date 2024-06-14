set -e

export DEBIAN_FRONTEND=noninteractive

pip install -c /env/python/constraints.txt -r /env/python/requirements-audit.txt
pip install --no-deps aequitas
