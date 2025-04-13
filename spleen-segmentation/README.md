pip install monai-deploy-app-sdk  # '--pre' to install a pre-release version.

# Clone monai-deploy-app-sdk repository for accessing examples.
git clone https://github.com/Project-MONAI/monai-deploy-app-sdk.git
cd monai-deploy-app-sdk

# Install necessary dependencies for simple_imaging_app
pip install matplotlib Pillow scikit-image

# Execute the app locally
python examples/apps/simple_imaging_app/app.py -i examples/apps/simple_imaging_app/input/brain_mr_input.jpg -o output

# Package app (creating MAP Docker image), using `-l DEBUG` option to see progress.
# Also please note that postfix will be added to user supplied tag for identifying CPU architecture and GPU type etc.
monai-deploy package examples/apps/simple_imaging_app -c examples/apps/simple_imaging_app/app.yaml -t simple_app:latest --platform x64-workstation -l DEBUG

# Run the app with docker image and an input file locally
## Copy a test input file to 'input' folder
mkdir -p input && rm -rf input/*
cp examples/apps/simple_imaging_app/input/brain_mr_input.jpg input/
## Launch the app
monai-deploy run simple_app-x64-workstation-dgpu-linux-amd64:latest -i input -o output