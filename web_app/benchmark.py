import asyncio
import random
import time
from pathlib import Path
import requests

# Replace with the URL of your FastAPI app
BASE_URL = "http://localhost:8000"
ENDPOINT_URL = f"{BASE_URL}/actions/ocr/extract_text_from_image"

# Number of concurrent requests
NUM_REQUESTS = 100

# Function to send a single image upload request
async def send_image_request(image_path):
    with open(image_path, "rb") as f:
        files = {"image": (f.name, f)}
        start_time = time.time()
        response = requests.post(ENDPOINT_URL, files=files)
        # Check for successful response (optional)
        # response.raise_for_status()
        end_time = time.time()
        return end_time - start_time

# Function to run concurrent requests
async def run_benchmark():
    tasks = []
    for i in range(NUM_REQUESTS):
        # Replace with your image file paths
        image_path = str(random.choice(list(Path('~/Desktop').glob('*.png'))))
        print(f"{image_path}")
        tasks.append(send_image_request(image_path))
    start_time = time.time()
    await asyncio.gather(*tasks)
    end_time = time.time()
    total_time = end_time - start_time
    return total_time, NUM_REQUESTS

# Run the benchmark and print results
async def main():
    total_time, num_requests = await run_benchmark()
    average_time = total_time / num_requests
    print(f"Processed {num_requests} images in {total_time:.2f} seconds.")
    print(f"Average processing time per image: {average_time:.4f} seconds.")

if __name__ == "__main__":
    asyncio.run(main())
