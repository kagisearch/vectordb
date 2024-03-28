# These commands will be run after the devcontainer is built.

# Install vectordb locally for development
python3 -m pip install -e .
apt-get install git ncdu wget curl
