FROM python:3.6

COPY requirements.txt /tmp
RUN python3.6 -m pip install --no-cache-dir --disable-pip-version-check -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

COPY . /bot

WORKDIR ./bot
ENTRYPOINT ["python3.6", "bot.py"]
