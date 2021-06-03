FROM ubuntu:18.04

RUN apt-get -y update && apt-get install -y --no-install-recommends \
    wget \
    python3-pip \
    python3-setuptools \
    nginx \
    ca-certificates \
    && rm -rf /var/lib/apt/list/*

RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

RUN pip --no-cache-dir install flask gunicorn Pillow boto3

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY predict /opt/program

# Copy model file in the image
# COPY test_dir/model /opt/ml/model

# Copy input file in the image
# COPY test_dir/predict /opt/ml/input

# Make required directory
RUN mkdir /opt/ml && \
    mkdir /opt/ml/model && \
    mkdir /opt/ml/input && \
    mkdir /opt/ml/output

WORKDIR /opt/program