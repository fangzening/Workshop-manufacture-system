# Base Image
FROM python:3.6

# create and set working directory
RUN mkdir /app
WORKDIR /app

# Add current directory code to working directory
ADD . /app/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8888



RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


ENV DJANGO_SETTINGS_MODULE="sfc.settings" 



COPY pynwrfc-2.0.6-cp36-cp36m-linux_x86_64.whl /pynwrfc-2.0.6-cp36-cp36m-linux_x86_64.whl

COPY nwrfcsdk /nwrfcsdk

# add pyrfc
ENV SAPNWRFC_HOME=/nwrfcsdk
ENV LD_LIBRARY_PATH=/nwrfcsdk/lib
ENV PATH="/nwrfcsdk/lib:${PATH}" 
RUN echo /usr/local/lib > /etc/ld.so.conf.d/local.conf && \
    ldconfig

# Install system dependencies



# install environment dependencies
RUN pip3 install --upgrade pip 
# COPY dependency file
COPY requirements.txt requirements.txt

# Install project dependencies
RUN pip install -r requirements.txt

RUN python -m pip install /app/pynwrfc-2.0.6-cp36-cp36m-linux_x86_64.whl

RUN cat /usr/local/lib/python3.6/site-packages/pyrfc/__init__.py

# Collect static files

RUN python3 manage.py collectstatic --noinput


# Apply database migrations

RUN python3 manage.py migrate

EXPOSE 8888
CMD gunicorn sfc.wsgi:application --bind 0.0.0.0:$PORT
