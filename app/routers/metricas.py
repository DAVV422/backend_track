from fastapi import APIRouter, HTTPException
from app.services.detectors import detectar_plataforma, Plataforma
from app.services.profiles.scraper_profile_facebook import ProfileFacebookScraper
from app.services.profiles.scraper_profile_instagram import ProfileInstagramScraper
from app.services.profiles.scraper_profile_tiktok import ProfileTikTokScraper

from app.services.publicaciones.scraper_facebook import FacebookScraper
from app.services.publicaciones.scraper_instagram import InstagramScraper
from app.services.publicaciones.scraper_tiktok1 import TikTokScraper

from pydantic import BaseModel

class ProfileRequest(BaseModel):
    url: str

router = APIRouter()


@router.post("/profile")
async def get_metricas_profile(request: ProfileRequest):
    plataforma = detectar_plataforma(request.url)

    if plataforma == Plataforma.FACEBOOK:
        service = ProfileFacebookScraper()
    elif plataforma == Plataforma.INSTAGRAM:
        service = ProfileInstagramScraper()
    elif plataforma == Plataforma.TIKTOK:
        service = ProfileTikTokScraper()
    else:
        raise HTTPException(status_code=400, detail="Plataforma no soportada")

    return service.get_profile(request.url)


@router.post("/publicacion")
async def get_metricas_publicacion(request: ProfileRequest):
    plataforma = detectar_plataforma(request.url)

    if plataforma == Plataforma.FACEBOOK:
        service = FacebookScraper()
    elif plataforma == Plataforma.INSTAGRAM:
        service = InstagramScraper()
    elif plataforma == Plataforma.TIKTOK:
        service = TikTokScraper()
    else:
        raise HTTPException(status_code=400, detail="Plataforma no soportada")

    return service.get_metrics(request.url)
