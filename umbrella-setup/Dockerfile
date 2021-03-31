FROM python:3.8

RUN apt-get update && \
    apt-get install -y \
        libglib2.0-0 \
        libnss3 \
        libgconf-2-4 \
        libfontconfig1 \
        firefox-esr

COPY geckodriver /usr/bin/geckodriver
RUN chmod 755 /usr/bin/geckodriver

RUN pip install selenium requests
WORKDIR /src
# COPY create_admin_user.py .
ENTRYPOINT ["python3"]
# CMD ["/src/create_admin_user.py"]