import uvicorn

class ServerRunner:
    @staticmethod
    def create_and_run_server(reflection_name: str, port: int, host: str = "127.0.0.1", reload=True):
        uvicorn.run(
            app=reflection_name,
            host=host,
            port=port,
            reload=reload
        )