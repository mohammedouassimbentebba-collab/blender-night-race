#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🎬 Starting Cloud Render Job in GitHub Codespaces..."
echo "=========================================================="

CORES=$(nproc)
echo "💻 Available CPU Cores: $CORES"

# Create output folder
mkdir -p output

# Check Blender binary
BLENDER_BIN=$(which blender)
if [ -z "$BLENDER_BIN" ]; then
    echo "❌ Error: blender executable not found!"
    exit 1
fi

echo "Using Blender: $($BLENDER_BIN --version | head -n 1)"

# Check if scene file or build script exists
if [ -f "build_scene.py" ]; then
    echo "🔨 Building/Updating 3D Race Scene in Blender..."
    xvfb-run -a $BLENDER_BIN --background --python build_scene.py -- -t $CORES
fi

# Render final animation if .blend file is ready
BLEND_FILE="output/cinematic_race.blend"
if [ -f "$BLEND_FILE" ]; then
    echo "🚀 Rendering cinematic animation (using $CORES threads with xvfb)..."
    xvfb-run -a $BLENDER_BIN --background "$BLEND_FILE" -t "$CORES" -a
    echo "✅ Rendering completed successfully! Check output/ directory."
else
    echo "ℹ️ Scene file $BLEND_FILE not found yet. Running python runner..."
    if [ -f "cinematic_film/render_movie.py" ]; then
        xvfb-run -a $BLENDER_BIN --background --python cinematic_film/render_movie.py
    fi
fi

echo "=========================================================="
echo "🎉 Film production complete! Download output/final_film.mp4"
echo "=========================================================="
