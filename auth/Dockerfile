# Use an appropriate Python version based on availability
FROM python:3.10-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY ./requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install -r requirements.txt \
    && rm -rf /root/.cache/pip

# Set environment variables
ENV SECRET_KEY=${SECRET_KEY}
ENV ALGORITHM=${ALGORITHM}
ENV ACCESS_TOKEN_EXPIRE_MINUTES=${ACCESS_TOKEN_EXPIRE_MINUTES}
ENV DATABASE_URI_AUTH=${DATABASE_URI_AUTH}

# Copy the rest of the app
COPY . /app/

# Start the app using Uvicorn
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
