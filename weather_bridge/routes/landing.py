from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def landing_page():
    return """
    <html>
        <head>
            <title>weather-bridge</title>
            <style>
                body { font-family: Arial; margin: 40px; background: #f5f5f5; }
                .box {
                    background: white; padding: 20px; border-radius: 10px;
                    max-width: 600px; box-shadow: 0 0 10px rgba(0,0,0,0.1);
                }
                h1 { color: #2c3e50; }
                a { color: #2980b9; font-weight: bold; }
            </style>
        </head>
        <body>
            <div class="box">
                <h1>🌤️ weather-bridge</h1>
                <p>A lightweight bridge for forwarding weather station data.</p>

                <h3>API Endpoints</h3>
                <ul>
                    <li><a href="/config">/config</a> – Show current configuration</li>
                    <li>POST <strong>/hook</strong> – Receive and forward weather data</li>
                </ul>

                <h3>Documentation</h3>
                <ul>
                    <li><a href="/docs">Swagger UI</a></li>
                    <li><a href="/redoc">ReDoc</a></li>
                </ul>

                <p style="margin-top:20px; color:#777;">weather-bridge is running 🎉</p>
            </div>
        </body>
    </html>
    """
