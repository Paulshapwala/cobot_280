#!/bin/bash
set -e

echo "🚀 Starting ROS Container..."

if [ -f "$HOME/setup.sh" ]; then
    bash "$HOME/setup.sh"
fi

echo "✅ Container ready!"
exec bash