FROM mcr.microsoft.com/devcontainers/base:ubuntu-24.04

# Avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install core runtime dependencies, OpenGL/Mesa software rasterizers, FFmpeg, and audio utilities
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    xz-utils \
    ffmpeg \
    libgl1 \
    libglu1-mesa \
    libglx-mesa0 \
    libosmesa6 \
    libegl1 \
    libsm6 \
    libxrender1 \
    libxinerama1 \
    libxi6 \
    libxfixes3 \
    libxkbcommon0 \
    libfontconfig1 \
    xvfb \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install official Blender Linux 64-bit release (matching desktop version 5.2.2 LTS)
ARG BLENDER_VERSION=5.2.2
ARG BLENDER_MAJOR=5.2
RUN mkdir -p /opt/blender && \
    wget -q https://download.blender.org/release/Blender${BLENDER_MAJOR}/blender-${BLENDER_VERSION}-linux-x64.tar.xz -O /tmp/blender.tar.xz && \
    tar -xJf /tmp/blender.tar.xz -C /opt/blender --strip-components=1 && \
    rm /tmp/blender.tar.xz && \
    ln -s /opt/blender/blender /usr/local/bin/blender

# Set environment variables for headless rendering and GPU/CPU optimization
ENV MESA_GL_VERSION_OVERRIDE=4.5
ENV MESA_GLSL_VERSION_OVERRIDE=450
ENV PYTHONUNBUFFERED=1

WORKDIR /workspaces/Blender
