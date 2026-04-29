from fastapi import APIRouter, WebSocket
from app.services.websocket.manager import manager

router = APIRouter()

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()

            # 🔥 broadcast to ALL users
            await manager.broadcast(f"User says: {data}")

    except:
        manager.disconnect(websocket)