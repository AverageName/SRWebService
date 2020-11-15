FROM ubuntu

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


RUN apt-get update && apt-get install -y --no-install-recommends python3.7 \
               python3-pip \
		       libgl1-mesa-glx \
		       libgtk2.0-dev

RUN pip3 install setuptools

RUN pip3 install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip3 install opencv-python

RUN pip3 install flask

ADD ./nn_microservice/api/* /nn_microservice/api/

CMD ["pwd"]

