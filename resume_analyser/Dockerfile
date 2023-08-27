# Use a base image with Python
FROM python:3.11.4

# Set up a working directory inside the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Copy the requirements file into the container
COPY requirements.txt /app

# Install project dependencies
RUN pip install -r requirements.txt

# Install spacy and download the en_core_web_sm model
RUN pip install -U spacy && python -m spacy download en_core_web_sm

# Specify the command to run your application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]