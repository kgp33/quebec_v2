# Quebec_v2

## Introduction

**Quebec_v2** is a financial analysis tool for equity portfolio pricing. It calculates the Sharpe Ratio of a given portfolio and provides pricing for stock portfolios. Portfolio data is provided in a specified `.json` format, enabling quick and easy manipulation of portfolio data.

---

## Quickstart

### Install Docker

Get Docker from the official documentation: [Get Docker](https://docs.docker.com/get-started/get-docker/)

### Build the Docker Container
```bash
docker build -t quebec_v2_app .
```

### Run the Docker Container
```bash
docker run -p 5000:5000 quebec_v2_app
```

### Access the Application

1. Open your browser and navigate to: [http://localhost:5000](http://localhost:5000).
2. Upload a `.json` portfolio file (ex: `stock_ex1.json`).

---

## Make your Custom Portfolio

Ensure your portfolio data is saved in a `.json` format following the [Quebec_v2 JSON Schema](https://github.com/kgp33/quebec_v2/blob/main/Schemas/stock-schema.json).

### Example JSON Format:
```json
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

### Upload Portfolio Data

1. Navigate to the application running at [http://localhost:5000](http://localhost:5000).
2. Upload your `.json` portfolio file.
3. Click "Upload" to view the analysis and generated graphs.

---

## Dependencies

- Docker
- Additional dependencies: [requirements.txt](https://github.com/kgp33/quebec_v2/blob/main/requirements.txt)

---

## Viewing UML Diagrams

To view diagrams in **VSCode**, you need to install the **PlantUML** extension. 

### Steps:

1. Install **Java** and **Graphviz** on your system.
2. Install the **PlantUML** extension in **VSCode**.
3. Open the diagram file.
4. Right-click anywhere in the code and select **"Preview Current Diagram"**.

You can also use free online PlantUML renderers to view the diagrams.

---

## Contributing

Contributions are welcome! For significant changes, please open an issue to discuss your ideas. 

### Steps to Contribute:
1. Fork the repository.
2. Make your changes.
3. Submit a pull request for review.

For more information, refer to the [CONTRIBUTING.md](https://github.com/kgp33/quebec_v2/blob/main/CONTRIBUTING.md).

---

## Additional Documentation

- **Coding Standards**: [Secure_Coding_Standard.md](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Secure_Coding_Standard.md)
- **Bandit Implementation**: [Bandit.md](https://github.com/kgp33/quebec_v2/blob/main/DOCS/Bandit.md)

---

## Developer Notes

### Using VSCode for Development

1. Run the application:
   ```bash
   python3 app.py
   ```

2. Ensure that development mode (`debug`) is set to `True`.

3. Use this setup to add and debug features effectively.

