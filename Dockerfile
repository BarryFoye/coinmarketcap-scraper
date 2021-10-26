FROM python:alpine3.9

WORKDIR /opt/coinmarketcap

# Copy files across
COPY project.toml /opt/coinmarketcap/
COPY requirements.txt /opt/coinmarketcap/
COPY setup.py /opt/coinmarketcap/
COPY README.md /opt/coinmarketcap/
COPY scripts /opt/coinmarketcap/

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m build \
    && pip install -e .
# RUN source ./scripts/init_db.sh

CMD [ "echo", "Welcom to the data model container!" ]
