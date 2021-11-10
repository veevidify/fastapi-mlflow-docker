from python:3.8-slim

WORKDIR /ml

# install conda for mlflow env
RUN apt-get update; apt-get install -y curl
RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda-installer.sh
RUN bash miniconda-installer.sh -b -p && rm miniconda-installer.sh

ENV PATH=/root/miniconda3/bin:${PATH}

RUN conda update -y conda

COPY . /ml
RUN conda init

# pg tools
RUN apt-get install -y libpq-dev gcc
RUN pip install mlflow sklearn numpy matplotlib pandas psycopg2

CMD ["mlflow", "backend"]
