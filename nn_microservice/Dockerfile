FROM ubuntu:18.04

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y --no-install-recommends python3.7 \
               python3-pip \
               wget \
		       libgl1-mesa-glx \
		       libgtk2.0-dev

RUN pip3 install --upgrade pip
RUN pip3 install setuptools

RUN wget https://download.pytorch.org/whl/cpu/torch-1.1.0-cp36-cp36m-linux_x86_64.whl
RUN wget https://download.pytorch.org/whl/cpu/torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

RUN pip3 install torch-1.1.0-cp36-cp36m-linux_x86_64.whl
RUN pip3 install torchvision-0.3.0-cp36-cp36m-linux_x86_64.whl

RUN pip3 install opencv-python \
                 matplotlib \
                 scipy==1.1.0 \
                 scikit-image \
                 tqdm

RUN pip3 install flask

ADD ./ .

CMD ["pwd"]

