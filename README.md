# Quebec_v2 Project

## Introduction
Quebec_v2 is a financial analysis tool for Equity Portfolio Pricing.  Quebec_v2 is a spin off
from Quebec.  Quebec_v2 prices stock portfolios and calculates the Sharpe Ratio of the given
portfolio.

## Quickstart

### Docker Setup

- Start by [getting docker](https://docs.docker.com/get-started/get-docker/)

- You can pull the image from dockerhub:

    `docker pull m1ntfish3r/quebec:latest`
    `docker pull m1ntfish3r/quebec:arm`
    `docker pull m1ntfish3r/quebec:amd`

- Or you can build the image on your own

    `docker build -t image_name .`

- Create a container and run it via shell:

    `docker run -it --name container_name image_name`

        examples:
        `docker run -it m1ntfish3r/quebec:latest`
        `docker run -it m1ntfish3r/quebec:arm`
        `docker run -it m1ntfish3r/quebec:amd`

- Exit the container shell:

    `exit`

- Restart the container:

    `docker start -i container_name`

### Prepare Input Data

Ensure portfolio data is in the following JSON format:

### Data Setup  

    1. Ensure the JSON files are formatted accourting to the Quebec_v2 JSON Schema
    2. *will need to update....  Place properly formated JSON files in the project directory.


### Upload specific portfolio data

To upload your portfolio data use the command below:
    `docker run -v /HOST/PATH: /CONTAINER/PATH -it <container_name>`

    example:
        `docker run -v /Users/lindseybaucum/Desktop/stock1.json:/quebec_v2/stock1.json -it m1ntfish3r/quebec:amd`


### Running the Application
To price an equity portfolio from root directory:

`python3 driver.py`

Unit tests:

`pytest`


### VSCode + Container

- Install 'Dev Containers' extention

- Start your container:

    `docker start container_name`

- Find Remote Explorer in your side bar

- Attach to your running container

