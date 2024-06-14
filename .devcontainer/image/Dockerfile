FROM python:3.12-slim as seismometer

RUN useradd --create-home --uid 1000 --shell /bin/bash seismo
ENV PATH=${PATH}:/home/seismo/.local/bin

# split copy to allow more caching of layers 
#COPY ./stagefiles /env
COPY ./stagefiles/layer.sh /env/layer.sh
RUN /bin/sh /env/layer.sh

USER seismo

COPY ./stagefiles/python /env/python
RUN pip install --no-cache-dir -c /env/python/constraints.txt -r /env/python/requirements.txt
RUN pip install --no-cache-dir -c /env/python/constraints.txt -r /env/python/requirements-dev.txt 

COPY ./stagefiles/audit_install.sh /env/audit_install.sh
RUN /bin/sh /env/audit_install.sh

# https://github.com/opencontainers/image-spec/blob/main/annotations.md
LABEL \
    org.opencontainers.image.vendor="Epic" \
    org.opencontainers.image.title="Seismometer" \
    org.opencontainers.image.description="Development container for AI Trust & Assurance Toolset"

WORKDIR /home/seismo/workspace
CMD /bin/bash
