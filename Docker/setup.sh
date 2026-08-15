#!/bin/bash
set -e

echo "🚀 ROS Setup Starting..."

# Source environment variables
if [ -f "$HOME/environment-variables.sh" ]; then
    source "$HOME/environment-variables.sh"
    echo "✅ Environment variables loaded"
fi

# Add to bashrc
if ! grep -q "environment-variables.sh" ~/.bashrc; then
    echo "source \$HOME/environment-variables.sh" >> ~/.bashrc
fi

echo "✅ Setup complete!"
source ~/.bashrc