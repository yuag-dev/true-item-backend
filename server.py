import asyncio
import websockets
import os

connected_clients = set()

async def handler(websocket):
    connected_clients.add(websocket)
    print(f"عميل جديد اتصل. العدد الحالي: {len(connected_clients)}")

    try:
        async for message in websocket:
            print(f"استلمت: {message}")
            if connected_clients:
                await asyncio.gather(
                    *[client.send(message) for client in connected_clients if client != websocket],
                    return_exceptions=True
                )
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        connected_clients.discard(websocket)
        print(f"عميل خرج. العدد الحالي: {len(connected_clients)}")


async def main():
    port = int(os.environ.get("PORT", 8765))
    async with websockets.serve(handler, "0.0.0.0", port):
        print(f"السيرفر شغال على بورت {port}")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())