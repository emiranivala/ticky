import os
import aiohttp

# Utility function to split files into smaller chunks
def split_large_file(file_path, chunk_size=50 * 1024 * 1024):
    file_size = os.path.getsize(file_path)
    chunk_count = (file_size // chunk_size) + (1 if file_size % chunk_size else 0)
    chunks = []
    with open(file_path, 'rb') as f:
        for i in range(chunk_count):
            chunk = f.read(chunk_size)
            chunk_name = f"{file_path}_part_{i+1}"
            with open(chunk_name, 'wb') as chunk_file:
                chunk_file.write(chunk)
            chunks.append(chunk_name)
    return chunks

# Asynchronous download handler
async def download_large_file(url, destination, progress_callback=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            with open(destination, 'wb') as file:
                downloaded = 0
                total = int(response.headers.get('Content-Length', 0))
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    file.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)
