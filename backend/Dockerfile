FROM python:3.7

RUN pip install --upgrade pip

RUN pip3 install flask \
                 numpy \
                 pillow \
                 requests

RUN pip3 install flask-mongoengine

ADD ./backend/api/* /backend/api/

CMD ["pwd"]

