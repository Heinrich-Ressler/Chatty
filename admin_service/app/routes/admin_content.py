from fastapi import APIRouter, Depends, Header, HTTPException, status
import httpx

router = APIRouter(prefix="/admin", tags=["Content Moderation"])

POST_SERVICE_URL = "http://post_service:8000"

def check_admin(x_role: str = Header(...)):
    if x_role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

@router.get("/reports", summary="Список жалоб")
async def get_reports(x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{POST_SERVICE_URL}/reports")
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch reports")
        return resp.json()

@router.delete("/posts/{post_id}", summary="Удалить пост")
async def delete_post(post_id: int, x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{POST_SERVICE_URL}/posts/{post_id}")
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Post not found")
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to delete post")
        return {"message": f"Post {post_id} deleted"}

@router.delete("/comments/{comment_id}", summary="Удалить комментарий")
async def delete_comment(comment_id: int, x_role: str = Depends(check_admin)):
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{POST_SERVICE_URL}/comments/{comment_id}")
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Comment not found")
        if resp.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to delete comment")
        return {"message": f"Comment {comment_id} deleted"}
