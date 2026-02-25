from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse

from api.limiter.limiter import limiter

from config.config import API_AUTH_URL, API_CLIENT_ID, API_CLIENT_SECRET, API_REDIRECT_URL, API_TOKE_URL, API_API_ME

import requests

router = APIRouter(prefix="/oauth")


@router.get("/login")
@limiter.limit("3/minute")
async def login(request: Request):
    url = (
        f"{API_AUTH_URL}"
        f"?client_id={API_CLIENT_ID}"
        f"&redirect_uri={API_REDIRECT_URL}"
        "&response_type=code"
        "&scope=slack_id"
    )
    return RedirectResponse(url)

@router.get("/callback")
@limiter.limit("3/minute")
async def callback(request: Request):
    code = request.query_params.get("code")

    token_res = requests.post(
        API_TOKE_URL,
        json={
            "client_id": API_CLIENT_ID,
            "client_secret": API_CLIENT_SECRET,
            "redirect_uri": API_REDIRECT_URL,
            "code": code,
            "grant_type": "authorization_code"
        },
    )

    token_data = token_res.json()
    print(token_data)
    access_token = token_data.get("access_token")

    user_res = requests.get(
        API_API_ME,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user = user_res.json()
    print(user)
    slack_id = user.get("identity", {}).get("slack_id")

    if not slack_id:
        raise HTTPException(status_code=400, detail="Slack not connected")
    
    print(slack_id)

    return {"success": True, "slack_id": slack_id}