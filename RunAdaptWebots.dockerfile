# Derive from the webots enriched adapt
FROM adapt as base

# Update the OpenGL drivers
RUN apt-get install -y libglu1-mesa-dev freeglut3-dev mesa-common-dev mesa-utils libgl1-mesa-glx

# Run the webots appliation
CMD webots