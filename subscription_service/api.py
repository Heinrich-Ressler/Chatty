from fastapi import APIRouter, HTTPException, Request
import crud, schemas, clients


router = APIRouter()

@router.post("/subscribe/{user_id}")
async def subscribe(user_id: int, request: Request):
    current_user = await clients.get_current_user_id(request)
    if user_id == current_user:
        raise HTTPException(status_code=400, detail="Can't subscribe to yourself")
    try:
        await crud.subscribe(follower_id=current_user, user_id=user_id)
    except:
        raise HTTPException(status_code=409, detail="Already subscribed")
    return {"message": "Subscribed"}

@router.delete("/unsubscribe/{user_id}")
async def unsubscribe(user_id: int, request: Request):
    current_user = await clients.get_current_user_id(request)
    await crud.unsubscribe(follower_id=current_user, user_id=user_id)
    return {"message": "Unsubscribed"}

@router.get("/subscriptions/following")
async def following(request: Request):
    current_user = await clients.get_current_user_id(request)
    return await crud.get_following(user_id=current_user)

@router.get("/feed", response_model=list[schemas.Post])
async def feed(request: Request):
    current_user = await clients.get_current_user_id(request)
    user_ids = await crud.get_following(user_id=current_user)
    posts = await clients.fetch_posts(user_ids)
    return posts
