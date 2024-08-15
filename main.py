# Getting started with creating an API for a fictional social media site where users get to post messages 

from typing import Optional
from fastapi import FastAPI,Response,status, HTTPException
# from fastapi.params import Body - Not required anymore since we're using pydantic

'''
 It's a pain to get all the values we need from the body as we can see from the above, 
 and at this point  the client can basically send whatever they want to us. this data also isn't getting validated.
 To fix this, we need to force the client to send data in schema that we expect. 
 Schemas explicitly define what the data should look like - should we get anything other than what we expect, ERROR.

 Enter pydantic
 '''
from pydantic import BaseModel # pydantic helps with data validation
from random import randrange # for testing the api, random number to update the id

#create an instance of fasp api

app = FastAPI() 

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

#using this global variable to store the posts in memeory for now until I create the database
my_posts = [{"title": "titile of post 1", "contents": "content of post 1", "id":1},
            {"title": "favorite food", "contents": "jeqe", "id":2}] 

def post_locator(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        

def find_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


def delete_post(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get("/") #path operation aka route for the get method
def read_root(): #path operation function logic
    return {"message": "wecome to my api"} # what the call returns to the user

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post): # this is how we extract data from the body the client sent to us
    post_dict = post.model_dump()
    post_dict['id'] = randrange(10000000)
    my_posts.append(post_dict)
    return{"data": my_posts}

#lets see how we can get a single post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = post_locator(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the message with id {id} was not found")
    return{"post_detail": post}


    #now lets create the functionality for deleting a single post

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index_to_delete = find_post(id)
    if index_to_delete == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"the message with id {id} was not found")
    my_posts.pop(index_to_delete)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


 # functionality for updating a single post
@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    return {"message": "post {id} updated" }
     
