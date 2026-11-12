
import time

from curl_cffi import requests
from curl_cffi.requests import Session

__all__ = ["SESSION", "get"]

FLARESOLVERR_URL = "http://localhost:8191/v1"
BOOTSTRAP_URLS = [
    "https://api.asurascans.com/api/series",
    "https://cdn.asurascans.com/asura-images/chapters"
]

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "priority": "u=1, i",
    "referer": "https://asuracomics.com/comics",
}


def solve_cloudflare(session: Session, url: str) -> requests.Response:
    """Bootstrap through FlareSolverr and synchronize cookies."""

    response = requests.post(
        FLARESOLVERR_URL,
        json={
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000,
        },
        timeout=70,
    )
    response.raise_for_status()

    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(
            f"FlareSolverr failed: {data.get('message', data)}"
        )

    solution = data["solution"]

    # Keep the browser's User-Agent consistent with its cookies.
    if solution.get("userAgent"):
        session.headers["User-Agent"] = solution["userAgent"]

    # Import all cookies into curl_cffi's cookie jar.
    for cookie in solution.get("cookies", []):
        # print(cookie["name"], cookie["value"])
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path") or "/",
            secure=cookie.get("secure", False),
        )

    # Reconstruct the initial response.
    result = requests.Response()
    result.status_code = solution["status"]
    result._content = solution["response"].encode("utf-8")
    result.url = solution["url"]
    result.headers.update(solution.get("headers", {}))

    return result


def create_session() -> Session:
    session = Session(
        impersonate="chrome",
        headers=HEADERS,
        timeout=30,
    )

    # First request goes through FlareSolverr.
    for url in BOOTSTRAP_URLS:
        solve_cloudflare(session, url)

    return session


SESSION = create_session()


def get(url: str, **kwargs) -> requests.Response:
    """GET with retries and FlareSolverr fallback."""

    for attempt in range(6):
        response = SESSION.get(url, **kwargs)

        if response.status_code not in (429, 502, 503, 504):
            return response

        if response.status_code == 403:
            break

        if attempt < 5:
            time.sleep(2 * (2 ** attempt))

    # Refresh Cloudflare clearance if necessary.
    solve_cloudflare(SESSION, url)

    return SESSION.get(url, **kwargs)
