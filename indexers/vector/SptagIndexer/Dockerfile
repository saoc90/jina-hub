FROM jinaai/jina:devel

# build sptag
WORKDIR /app
RUN apt-get update && apt-get -y install wget build-essential python3-dev python3-pip git swig libboost-all-dev software-properties-common

RUN apt-get install libboost1.67 libboost1.67-dev

RUN wget https://cmake.org/files/v3.15/cmake-3.15.5.tar.gz && \
    tar zvxf cmake-3.15.5.tar.gz && \
    cd cmake-3.15.5 && \
    ./bootstrap && \
    make -j2 && make install

RUN git clone https://github.com/microsoft/SPTAG.git
RUN cd SPTAG && mkdir build && cd build && cmake .. && make -j2 && ls .. && mv ../Release /app

# so python can find the SPTAG module
ENV PYTHONPATH=/app/Release

# setup the workspace
COPY . /workspace
WORKDIR /workspace

# install the third-party requirements
RUN pip install -r requirements.txt

# for testing the image
RUN pip install pytest && pytest

ENTRYPOINT ["jina", "pod", "--uses", "config.yml"]