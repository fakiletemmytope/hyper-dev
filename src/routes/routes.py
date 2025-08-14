import asyncio
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from src.validator.user import UserInfoData
from src.helper.db import get_client  # noqa: F401
from src.helper.defi_functions import clients
from src.validator.defi import Protocol
from src.helper.functions import (
    process_defi,
    get_defi_from_db,
)
from src.helper.user_functions import all_user_date

router = APIRouter(prefix="/api")


@router.websocket("/get-defi")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        try:
            # Send initial data immediately
            initial_data = await get_defi_from_db()
            initial_data = Protocol.model_validate(initial_data)
            await websocket.send_text(initial_data.model_dump_json())
        except Exception as db_err:
            # Send DB error instead of killing WS
            await websocket.send_text(
                f'{{"error": "DB fetch failed: {db_err}"}}',
            )

        # Keep connection alive by waiting indefinitely
        # Periodic updates from notify_clients will keep the socket active
        while True:
            await asyncio.sleep(3600)  # Long sleep to minimize CPU usage

    except WebSocketDisconnect:
        pass
    except Exception as e:
        raise HTTPException(details=f"WebSocket error: {e}")
    finally:
        clients.discard(websocket)


@router.get("/user-info")
def user_info(data: UserInfoData):
    data = data.model_dump()

    value = all_user_date(**data)
    return value


@router.get("/defi")
def home():
    value = process_defi()
    try:
        client = get_client()
        database = client["defi-db"]
        collection = database["defi"]
        collection.insert_one(value.model_dump())
    except Exception as e:
        raise HTTPException(details=str(e))
    finally:
        return value
