# ROS Humble Development Container Setup

This is a complete development environment for ROS Humble that persists across container restarts.

## Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Builds the image with base ROS packages |
| `docker-compose.yml` | Manages container, volumes, and networking |
| `.devcontainer/devcontainer.json` | VS Code integration |
| `setup.sh` | Main orchestrator script (run on container startup) |
| `environment-variables.sh` | All environment variables (sourced by setup.sh) |
| `requirements.txt` | List of packages to install (actively maintained) |
| `requirements-python.txt` | Python packages to install with pip |

---

## Quick Start

### 1. First Time Setup

```bash
# Build and start the container
docker-compose up -d

# Connect to it
docker-compose exec ros-humble bash

# Run setup (installs packages, sets environment)
./setup.sh

# You're done! Container is ready
```

### 2. After Restarting PC

```bash
# Container volumes are persistent, just restart it
docker-compose up -d

# Connect
docker-compose exec ros-humble bash

# Everything from before is still there!
```

---

## How Persistence Works

### What's Saved (Named Volumes):
- **`ros-workspace`** → `/home/ws` (your code, builds)
- **`ros-home`** → `/home/shapzonlinux` (configs, bashrc)
- **`ros-apt-cache`** → Downloaded `.deb` files (speed up reinstalls)
- **`ros-apt-lists`** → Package metadata

### What's NOT Saved:
- Packages installed at runtime (unless in volumes)
- Environment variables (unless added to `environment-variables.sh`)

**Solution:** Update `environment-variables.sh` and `requirements.txt` before exiting!

---

## Workflow: Installing New Packages

### Step 1: Install the Package

```bash
docker-compose exec ros-humble bash

# Inside container:
sudo apt install ros-$ROS_DISTRO-rmw-cyclonedds-cpp
sudo apt install gazebo
```

### Step 2: Check What You Installed

```bash
sudo apt-mark showmanual
```

This shows all manually installed packages.

### Step 3: Update requirements.txt

Add the packages to `~/requirements.txt`:

```bash
echo "ros-humble-rmw-cyclonedds-cpp" >> ~/requirements.txt
echo "gazebo" >> ~/requirements.txt
```

Or edit it manually:
```bash
nano ~/requirements.txt
```

### Step 4: Update Environment Variables (If Needed)

If you added environment variables during the session:

```bash
nano ~/environment-variables.sh
```

Example:
```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export GAZEBO_MODEL_PATH=/home/ws/models:$GAZEBO_MODEL_PATH
```

### Step 5: Commit to Git

```bash
git add requirements.txt environment-variables.sh
git commit -m "Added RMW CycloneDDS and Gazebo"
```

### Step 6: Next Time You Restart

```bash
docker-compose up -d
docker-compose exec ros-humble bash
./setup.sh  # Reads requirements.txt, installs everything automatically
```

---

## Environment Variables

### Adding Permanent Environment Variables

Edit `~/environment-variables.sh`:

```bash
nano ~/environment-variables.sh
```

Add your variables:
```bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_DOMAIN_ID=42
export GAZEBO_MODEL_PATH=/home/ws/models:$GAZEBO_MODEL_PATH
export MY_CUSTOM_VAR=my_value
```

Then source it:
```bash
source ~/environment-variables.sh
```

Or restart the container - `setup.sh` sources it automatically.

### View Current Variables

```bash
# All variables
env | grep ROS
env | grep GAZEBO

# Or check the file
cat ~/environment-variables.sh
```

---

## Installing Different Package Types

### System Packages (apt-get)

```bash
sudo apt install ros-$ROS_DISTRO-moveit
# Add to: ~/requirements.txt
```

### Python Packages (pip)

```bash
pip install numpy scipy opencv-python
# Add to: ~/requirements-python.txt
```

### From Source (in workspace)

```bash
cd ~/ws/src
git clone https://github.com/user/repo
cd ~/ws
colcon build
# This is saved in ros-workspace volume automatically
```

---

## 🐛 Troubleshooting

### Package Disappeared After Restart

**Cause:** You installed it but didn't add it to `requirements.txt`

**Fix:** 
```bash
# Check what was installed
sudo apt-mark showmanual | grep <package-name>

# Add to requirements.txt
echo "<package-name>" >> ~/requirements.txt

# Reinstall
./setup.sh
```

### Environment Variable Not Persisting

**Cause:** You exported it in the shell but didn't add to `environment-variables.sh`

**Fix:**
```bash
# Add to the file
echo 'export MY_VAR=value' >> ~/environment-variables.sh

# Source it
source ~/environment-variables.sh
```

### Container Won't Start

```bash
# Check logs
docker-compose logs ros-humble

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

### Storage Is Too Large

```bash
# Clean up build artifacts (temporary files)
cd ~/ws
colcon clean build
colcon clean install

# Or clean everything
colcon clean all

# This removes temporary files but keeps your code
```

---

## Storage Usage

Typical sizes:
- **Persistent** (always on disk): ~5-8 GB
  - Code, builds, configs, cached packages
  
- **Runtime** (when container running): ~25 GB
  - Includes temporary build files, running processes
  
- **After `colcon clean all`**: ~8-10 GB
  - Temporary files removed, code preserved

---

## Typical Development Cycle

```
Session 1:
├─ docker-compose up -d
├─ docker-compose exec ros-humble bash
├─ ./setup.sh (installs from requirements.txt)
├─ Develop code in ~/ws/
├─ apt install gazebo
├─ Edit requirements.txt
├─ git commit
└─ exit

PC Restart:
├─ docker-compose up -d (all volumes restored!)
├─ docker-compose exec ros-humble bash
├─ ./setup.sh (reads updated requirements.txt)
├─ All packages reinstalled, ready to go
└─ Continue developing
```

---

## Checklist Before Exiting Container

- [ ] Added new packages to `~/requirements.txt`
- [ ] Updated `~/environment-variables.sh` if needed
- [ ] Ran `git add requirements.txt environment-variables.sh`
- [ ] Ran `git commit -m "Updated dependencies"`
- [ ] Tested that `./setup.sh` works (optional)

---

## Important Notes

1. **Always update requirements.txt** - Don't rely on packages persisting without being recorded
2. **Commit regularly** - Track your changes in git
3. **Use docker-compose** - Not just raw `docker` commands
4. **Check environment-variables.sh** - It runs first in setup.sh
5. **Name your volumes** - This is what makes persistence work

---

## VS Code Integration

### Using VS Code with the Container

1. Install "Dev Containers" extension in VS Code
2. Open your workspace folder in VS Code
3. VS Code detects `.devcontainer/devcontainer.json`
4. Click "Reopen in Container" button
5. VS Code connects to `ros-humble` container
6. `postAttachCommand` runs `setup.sh` automatically

### Or Connect to Running Container

1. `docker-compose up -d` (start container)
2. In VS Code: Command Palette → "Dev Containers: Attach to Running Container"
3. Select `ros-humble`
4. Done!

---

## References

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Dev Containers in VS Code](https://code.visualstudio.com/docs/remote/containers)