# These commands will be run after the devcontainer is built.

python3 -m pip install git+https://github.com/vioshyvo/mrpt/
python3 -m pip install -e . # Install vectordb locally
