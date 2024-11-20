# quebec_v2
Equity Portfolio Pricing

To price an equity portfolio from root directory:

`python3 driver.py`

To run unit tests:

`pytest`

### Diagrams
To view the diagrams in VSCode, you'll need to install the PlantUML extension in VSCode to render them. After install:

1. Open file
2. Right click anywhere in the code
3. Click "Preview Current Diagram

You will also need to have java and graphviz installed to view these diagrams using the PlantUML extension in VSCode. You can also find free PlantUML renderers online.

### Docker Setup

- Start by [getting docker](https://docs.docker.com/get-started/get-docker/)

- You can pull the image from dockerhub:

    `docker pull m1ntfish3r/quebec:latest`

- Or you can build the image on your own

    `docker build -t image_name .`

- Create a container and run it via shell:

    `docker run -it --name container_name image_name`

    (if you pulled it from dockerhub then image name will be `m1ntfish3r/quebec:latest`)

- Exit the container shell:

    `exit`

- Restart the container:

    `docker start -i container_name`

### VSCode + Container

- Install 'Dev Containers' extention

- Start your container:

    `docker start container_name`

- Find Remote Explorer in your side bar

- Attach to your running container