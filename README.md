# quebec_v2
Equity Portfolio Pricing

To price an equity portfolio from root directory:

`python3 -m PriceApp.price`

### Docker Setup

- Start by [getting docker](https://docs.docker.com/get-started/get-docker/)
- You can pull the image from dockerhub by `docker pull m1ntfish3r/quebec:latest`
- Or you can build the image on your own by `docker build -t image_name .`
- Create a container and run it via shell by `docker run -it --name container_name image_name` (if you pulled it from dockerhub then image name will be `m1ntfish3r/quebec:latest`)
- Exit the container shell by simply typing `exit`
- Restart the container by `docker start -i container_name`