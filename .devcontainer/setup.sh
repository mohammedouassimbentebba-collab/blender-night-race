#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "🚀 Initializing Blender 3D Cloud Studio in GitHub Codespaces..."
echo "=========================================================="

# Check Blender installation
if command -v blender &> /dev/null; then
    echo "✅ Blender found: $(blender --version | head -n 1)"
else
    echo "⚠️ Blender not in PATH, checking /opt/blender..."
    if [ -f "/opt/blender/blender" ]; then
        sudo ln -sf /opt/blender/blender /usr/local/bin/blender
        echo "✅ Blender linked successfully!"
    else
        echo "❌ Blender installation not found. Installing via apt fallback..."
        sudo apt-get update && sudo apt-get install -y blender
    fi
fi

# Ensure Python requirements are installed in container
pip3 install --no-cache-dir requests numpy urllib3 mcp || true

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

echo "=========================================================="
echo "🎉 Environment ready! You can render the film in cloud by running:"
echo "   bash scripts/render_cloud.sh"
echo "=========================================================="
