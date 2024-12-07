from flask import Flask, request, render_template, send_file
import os
import PriceApp.price as price


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Quebec V2</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 50px;
            }
            h1 {
                color: #333;
            }
            form {
                margin-top: 20px;
            }
            button {
                padding: 10px 20px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <h1>Quebec V2</h1>
        <p>Upload a JSON file to generate a stock price graph.</p>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".json">
            <br><br>
            <button type="submit">Upload JSON</button>
        </form>
    </body>
    </html>
    '''


@app.route('/upload', methods=['POST'])
def upload_file():
    global counter
    file = request.files['file']
    if file and file.filename.endswith('.json'):
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        counter += 1
        price.calculate_value_sharpe(filepath, counter=counter)
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Quebec V2 - Graph</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                h1 {
                    color: #333;
                }
                img {
                    max-width: 90%;
                    height: auto;
                    margin-top: 20px;
                }
                a {
                    text-decoration: none;
                    color: #007BFF;
                }
                a:hover {
                    color: #0056b3;
                }
            </style>
        </head>
        <body>
            <h1>Portfolio</h1>
            <img src="/graph" alt="Stock Graph">
            <br><br>
            <a href="/">Go Back</a>
        </body>
        </html>
        '''
    return "Invalid file format. Please upload a valid JSON file.", 400


@app.route('/graph')
def get_graph():
    global counter
    graph_dir = os.path.abspath("graphs")
    file_path = os.path.join(graph_dir, f"graph_{counter}.png")
    return send_file(file_path, mimetype='image/png')


if __name__ == '__main__':
    global counter
    counter = 0
    app.run(host='0.0.0.0', port=5000, debug=True)
