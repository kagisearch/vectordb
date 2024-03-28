# Use the Pangeo base image
ARG PANGEO_BASE_IMAGE_TAG=master
FROM pangeo/base-image:${PANGEO_BASE_IMAGE_TAG}

# Copy the environment.yaml file into the Docker image
COPY environment.yaml /tmp/environment.yaml

# Use the conda command to create a new environment from the environment.yaml file
RUN conda env create -f ~/.devcontainer/environment.yaml
RUN conda init bash
RUN echo "conda activate ssec-scipy2024" >> ~/.bashrc
