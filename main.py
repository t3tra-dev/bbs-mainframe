import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

RSA_KEY = RSA.generate(2048)
PRIVATE_KEY = RSA_KEY.export_key(format="PEM",pkcs=8)
PUBLIC_KEY = RSA_KEY.publickey().export_key(format="PEM",pkcs=8)
KEY_HEADER = "-----BEGIN PUBLIC KEY-----"
KEY_FOOTER = "-----END PUBLIC KEY-----"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では制限
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")  # AWSのELBでヘルスチェックに使う
async def health_check():
    return {"status": "ok"}

@app.get("/public_key")
async def get_public_key():
    return {"public_key": PUBLIC_KEY.decode().replace("\n", "").replace(KEY_HEADER, "").replace(KEY_FOOTER, "")}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.send_message("Client disconnected")
