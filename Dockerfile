ARG PYTHON_IMAGE
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE}:${PYTHON_IMAGE_VERSION}

WORKDIR /opt/rsrc

COPY rsrc/ rsrc/
COPY tests/ tests/
COPY README.md .
COPY requirements-tests.txt .
COPY requirements.txt .
COPY setup.cfg .
COPY .coveragerc .
COPY setup.py .

RUN pip install -r requirements-tests.txt
RUN pip install -r requirements.txt
