from utils import get_status_code

if __name__ == "__main__":
    url = "https://example.com"
    status = get_status_code(url)
    print(f"Status code for {url}: {status}")
