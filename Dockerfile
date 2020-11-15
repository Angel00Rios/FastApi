FROM python:3.9

COPY . /app

# Upgrade pip and install packages
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /app/requirements.txt

# add python api path
ENV PYTHONPATH=/app/app

# run
CMD ["sh", "/app/api.sh"]