FROM python:3.9

# Set the working directory to /usr/src/app.
WORKDIR /code

# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./

# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt
RUN playwright install
RUN playwright install-deps
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .