from pyngrok import ngrok
import uvicorn, atexit
from dotenv import set_key
from pathlib import Path

env_path = Path("../../.env")

# Arranca ngrok
tunnel = ngrok.connect("8000")
public_url = tunnel.public_url
print("Ngrok URL:", public_url)
set_key(str(env_path), "NGROK_URL", str(public_url))
atexit.register(ngrok.kill)

# Arranca o servidor FastAPI (importando a app)
uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=False)
