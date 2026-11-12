from utils.session import SESSION
from pathlib import Path

def download(url: str, filename: Path | str):
    res = SESSION.get(
        url,
        headers={
            "referer": "https://asurascans.com/",
            "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
        },
        stream=True
    )
    # print(url)
    # print(res.text)
    
    
    # res1 = SESSION.get(
    #     url,
    #     headers={
    #         "referer": "https://asurascans.com/",
    #         "accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    #     },
    # )

    # print(res1.status_code)
    # print(res1.headers)
    # print(res1.text[:1000] if res1.status_code != 200 else "OK")
    
    # print("--logging done--")

    try:
        res.raise_for_status()

        with open(filename, "wb") as f:
            for chunk in res.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)
    finally:
        res.close()
