# These commands will be run after the devcontainer is built.

# Install vectordb locally for development
python3 -m pip install --user -r requirements.txt # Install required packages
python3 -m pip install pre-commit nox # Install development tools
python3 -m pip install -e . # Install vectordb locally
