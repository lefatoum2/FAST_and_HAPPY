# Fast_and_Happy

![](https://static.hitek.fr/img/actualite/ill_m/357630542/walkerdiesel.jpg)
* [1. Exceptions : HTTPException](#exceptions)
* [2. Regex](#regex)
* [3. Validator and Number Validators](#validator)


## 1. Exceptions : HTTPException<a class="anchor" id="exception"></a>

https://umbraco.com/knowledge-base/http-status-codes/

#### Example
```python
from fastapi.exceptions import HTTPException
...
image_url_types = ['absolute', 'relative']


@router.post('', response_model=PostDisplay)
def create(request: PostBase, db: Session = Depends(get_db), current_user: UserAuth = Depends(get_current_user)):
    if not request.image_url_type in image_url_types:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                            detail="Le paramètre de image_url_type peut seulement prendre une valeur absolue('absolute') ou relative('relative'). ")
    return db_post.create(db, request)
```

## 2. Regex <a class="anchor" id="regex"></a>
## 3. Validator and Number Validators<a class="anchor" id="validator"></a>
