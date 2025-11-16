from enum import Enum


class Plataforma(str, Enum):
    FACEBOOK = "facebook"
    INSTAGRAM = "instagram"
    TIKTOK = "tiktok"
    UNKNOWN = "unknown"


def detectar_plataforma(url: str) -> Plataforma:
    url_lower = url.lower()

    if "facebook.com" in url_lower:
        return Plataforma.FACEBOOK
    if "instagram.com" in url_lower:
        return Plataforma.INSTAGRAM
    if "tiktok.com" in url_lower:
        return Plataforma.TIKTOK

    return Plataforma.UNKNOWN
