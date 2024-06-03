# Pull base image.
FROM python:3.10

# Set default WORKDIR in container
WORKDIR /home/app

# Install package requirements
COPY requirements.txt .
# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Update the repository
COPY . /home/app

# Set the command to run preprocess.py
CMD ["python", "preprocess.py"]
