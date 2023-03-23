import hashlib
from fastapi import FastAPI, HTTPException
import models
import schemas
import database as db
import uvicorn

app = FastAPI()

db.Base.metadata.create_all(db.engine)


@app.post('/create-user')
def create_user(user: schemas.User):
    password = hashlib.sha256(user.password.encode()).hexdigest()
    newuser = models.Users(name=user.name, email=user.email, password=password)
    db.session.add(newuser)
    db.session.commit()
    db.session.refresh(newuser)
    return newuser


@app.get('/get-users')
def get_users():
    users = db.session.query(models.Users).all()
    return users


@app.get('/get-users/{id}')
def get_user(id: int):
    user = db.session.query(models.Users).filter(models.Users.id == id).first()
    return user


@app.put('/update-user/{id}')
def update_user(user: schemas.User, id:int):
    password = hashlib.sha256(user.password.encode()).hexdigest()
    theuser = db.session.query(models.Users).filter(models.Users.id == id).first()
    theuser.name = user.name
    theuser.email = user.email
    theuser.password = password

    db.session.commit()
    db.session.refresh(theuser)

    return theuser


@app.delete('/delete-user/{id}')
def delete_user(id:int):
    user = db.session.query(models.Users).filter(models.Users.id == id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return {'Effacé'}
    return {'User non trouvé'}


if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)