
def main():
    # Allow running this file directly without installing the package.
    from pathlib import Path
    import sys

    src_dir = Path(__file__).resolve().parents[2]
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    import uvicorn
    
    uvicorn.run(
        "realesrgan_http_api.http.server:svr",
        host="localhost",
        port=8080,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
