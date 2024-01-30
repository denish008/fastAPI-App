from fastapi import Depends, Response, status, HTTPException, APIRouter
from .. import models, oauth2, schemas
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2

router = APIRouter(
    tags=['Posts'],
    prefix="/posts"
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

#-----------------------------------------------------------------------------------------------------------------------------------#

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post : schemas.PostBase, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id,**new_post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#-----------------------------------------------------------------------------------------------------------------------------------#

@router.get("/{id}", response_model=schemas.Post) # id - path parameter
def get_post(id : int, db : Session = Depends(get_db), user_id : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    return post

#-----------------------------------------------------------------------------------------------------------------------------------#

@router.put("/{id}", response_model=schemas.Post)
def update_post(id : int, upd_post : schemas.PostBase, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id : {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requested action not authorized")
    
    post_query.update(upd_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

#-----------------------------------------------------------------------------------------------------------------------------------#

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    del_post = post_query.first()

    if del_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} does not exist")
    
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Requested action not authorized")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)