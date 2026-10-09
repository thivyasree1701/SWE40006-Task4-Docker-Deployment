from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SWE40006 Docker Deployment</title>

        <style>
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: Arial, sans-serif;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                background: linear-gradient(135deg, #071a2f, #0b4f8a);
                color: white;
            }

            .card {
                width: 700px;
                padding: 50px;
                text-align: center;
                background: rgba(255,255,255,0.10);
                border: 1px solid rgba(255,255,255,0.20);
                border-radius: 24px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.35);
            }

            .docker {
                font-size: 75px;
                margin-bottom: 15px;
            }

            h1 {
                font-size: 42px;
                margin-bottom: 10px;
            }

            .subtitle {
                color: #93c5fd;
                font-size: 20px;
                margin-bottom: 30px;
            }

            .details {
                text-align: left;
                background: rgba(0,0,0,0.20);
                border-radius: 15px;
                padding: 25px 30px;
                line-height: 2;
            }

            .label {
                color: #93c5fd;
                font-weight: bold;
            }

            .status {
                display: inline-block;
                margin-top: 30px;
                padding: 12px 25px;
                background: #16a34a;
                border-radius: 30px;
                font-weight: bold;
            }

            footer {
                margin-top: 30px;
                color: #cbd5e1;
            }
        </style>
    </head>

    <body>
        <div class="card">

            <div class="docker">🐳</div>

            <h1>Hello World from Docker!</h1>

            <p class="subtitle">Python Flask Web Application</p>

            <div class="details">
                <p><span class="label">Student:</span> Thivyasree A/P Sunder</p>
                <p><span class="label">Student ID:</span> 105685114</p>
                <p><span class="label">Unit:</span> SWE40006 - Software Deployment and Evolution</p>
                <p><span class="label">Task:</span> Task 4.2 - Python Web Application</p>
                <p><span class="label">Runtime:</span> Python 3.13</p>
                <p><span class="label">Framework:</span> Flask</p>
                <p><span class="label">Container Port:</span> 5000</p>
            </div>

            <div class="status">
                ✓ Docker Container Running
            </div>

            <footer>
                Containerised using Python, Flask and Docker
            </footer>

        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)