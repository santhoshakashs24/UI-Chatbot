# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /home/associate/UI-Chatbot

# Copy the current directory contents into the container at /home/associate/UI-Chatbot
COPY . /home/associate/UI-Chatbot

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-setuptools \
    python3-dev \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-pulseaudio \
    x11-xserver-utils \
    xvfb \
    xclip \
    xsel && \
    rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the display environment variable
ENV DISPLAY=:99

# Start Xvfb and run the Kivy app
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & python lseg_Chatbot.py"]

