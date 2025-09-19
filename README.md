🥠 Fortune Cookie API

A playful API built with FastAPI that generates random fortunes with funny, motivational, or startup-themed twists. Perfect for demos, side projects, or just a laugh.

🚀 Features

Generates random fortune cookie messages

Supports different vibes: funny, motivational, startup-themed

Free and Pro endpoints

Built with FastAPI and Uvicorn

Live demo running on Render

📦 Installation

Clone the repo:
git clone https://github.com/Carsten17/fortune-cookie-api.git

cd fortune-cookie-api

Install dependencies:
pip install -r requirements.txt

Run the app locally:
uvicorn app:app --reload

🔑 Endpoints

GET / → Root endpoint, returns a welcome message

GET /hello/{name} → Say hello with your name

POST /fortune → Generate a fortune cookie message

POST /fortune/pro → Generate multiple themed fortunes (Pro mode, requires API key)

🛠 Example Request

POST /fortune
{ "name": "Carsten", "vibe": "funny", "topic": "ai" }

Example Response:
{ "fortune": "Carsten, [ai] Even robots need coffee before solving bugs." }

💡 Use Cases

Add humor to your app or dashboard

Generate demo content for presentations

Show off API integrations in a fun way

📜 License

MIT License. Free to use, share, and modify.
