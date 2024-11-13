# quebec_v2
Equity Portfolio Pricing

To price an equity portfolio from root directory:

`python3 driver.py`

Unit tests:

`pytest`

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