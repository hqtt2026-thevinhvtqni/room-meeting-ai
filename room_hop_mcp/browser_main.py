import uvicorn

from room_hop_mcp.adapter.browser_server import create_browser_app


app = create_browser_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8001,
    )