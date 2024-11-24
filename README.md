# Quebec_v2 Project

## Introduction
Quebec_v2 is a financial analysis tool for Equity Portfolio Pricing.  Quebec_v2 prices stock portfolios and calculates the Sharpe Ratio of the given
portfolio. Portfolio data is provided in a specified .json format which allows quick and easy manipulation of portfolio data.

## Quickstart
The Quebec_v2 container image is available publically on Dockerhub.  Alternatively, you can clone the quebec_v2 repo [Here](https://github.com/kgp33/quebec_v2.git) and build the image locally.

### Install Docker

Here: [get docker](https://docs.docker.com/get-started/get-docker/)

### Download image from dockerhub

ARM: `docker pull m1ntfish3r/quebec:arm`

AMD: `docker pull m1ntfish3r/quebec:amd`

### Alternatively build the image manually
`git clone https://github.com/kgp33/quebec_v2.git`🦄

From the project Folder on your host machine:
`docker build -t image_name .`

### Run container

`docker run -it container_name/image_name`

ARM example: `docker run -it m1ntfish3r/quebec:arm`
AMD example: `docker run -it m1ntfish3r/quebec:amd`

> [!TIP]
> To exit the container shell:
> `exit`
> 
> To restart the contaier:
> `docker start -i container_name`
>
> Clear Docker cache and reset:
> `docker system prune -a`

### Prepare Input Data

Save your portfolio data as "stock.json" following the guidelines found in the [Quebec_v2 JSON Schema](https://github.com/kgp33/quebec_v2/blob/main/Schemas/stock-schema.json)

- Example: 
```ruby
[
    {
        "ticker": "AAPL", 
        "nShares": 10
    }, 
    {
        "ticker": "IBM",
        "nShares": 20
    },
    {
        "ticker": "MSFT",
        "nShares": 20
    },
    {
        "ticker": "GOOGL",
        "nShares": 20
    }
]
```

### Data Setup
Place properly formated JSON files in a file directory you can access from a terminal or cli.  
> [!NOTE]
> You will need the file path to the stock.json file to upload your data to the container.


### Upload specific portfolio data

To upload your portfolio data use the command below:
    `docker run -v /HOST/PATH: /CONTAINER/PATH -it <container_name>`

example:
    `docker run -v /Users/lindseybaucum/Desktop/stock.json:/quebec_v2/stock.json -it m1ntfish3r/quebec:amd`


### Running the Application

Once the container is running the price.py program can be run from the root directory.
`python3 PriceApp/price.py

> [!NOTE]
> To run the quebec_v2 test suite and ensure the application is performing as expected run `pyest`.
To price an equity portfolio from root directory:

## Dependencies
* Python: Quebec requires Python 3.8 or higher.
* Docker
* Additional dependencies [requirements.txt](https://github.com/kgp33/quebec_v2/blob/main/requirements.txt)

## Diagrams
To view the diagrams in VSCode, you'll need to install the PlantUML extension in VSCode to render them. After install:

1. Open file
2. Right click anywhere in the code
3. Click "Preview Current Diagram

You will also need to have java and graphviz installed to view these diagrams using the PlantUML extension in VSCode. You can also find free PlantUML renderers online.


## Contributing
Contributions are welcome! For significant changes, please open an issue first to discuss your ideas. Fork the repository and submit pull requests for review.
More information can be found in the [CONTRIBUTING.md](https://github.com/kgp33/quebec_v2/blob/main/CONTRIBUTING.md)🦑

## Additional Documentation
Coding Standards [Secure_Coding_Standard.md](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Secure_Coding_Standard.md)

Bandit Implementation [Bandit.md](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Bandit.md)🦝




### Developer Notes
#### VSCode + Container

- Install 'Dev Containers' extention

- Start your container:

    `docker start container_name`

- Find Remote Explorer in your side bar

- Attach to your running container

