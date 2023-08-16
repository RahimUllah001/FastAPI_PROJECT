from fastapi import FastAPI, Response, status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange





app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title":"tile of post no 1", "content":"content of the post no 1", "id":1},
              {"title": "my favorite foods" , "content":"pizzza", "id": 2}]    



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def root():
    return {"message": "Hello World"}



@app.get("/posts")
def get_posts():
    return {"DATA": my_posts}

# create post with random ids

@app.post("/posts" ,status_code= status.HTTP_201_CREATED)
def create_posts(post : Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000)
    my_posts.append(post_dict)

    return { "data ": post_dict}

#gettting specific post by id

@app.get("/posts/{id}")
def post_by_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail =  f"post with id no {id } not found")

    return {"new post": post}



#deleting a post
# for this we will first find a index in the array of thr required id so that we can delete 

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
     index= find_index_post(id)

     if index == None:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post not found with id no {id}")
     
     my_posts.pop(index)
     
     return {f"the post with id no. {id} succesfully deleted"}



# updating the existing post for this we use put method

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index= find_index_post(id)

    if index == None:
         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post not found with id no {id}")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {"datfffa": post_dict}
     
     



    