FROM python:3.11.4

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the entire app directory
COPY ./app .

# Set the volume for host files
VOLUME /host_files

# Set the entrypoint to run the main.py file
#ENTRYPOINT . /opt/venv/bin/activate && python main.py
#ENTRYPOINT [". /opt/venv/bin/activate","python","main.py"]
ENTRYPOINT ["/opt/venv/bin/python", "main.py"]

# in order to be able to pass arguments to app you need the following
CMD [""]