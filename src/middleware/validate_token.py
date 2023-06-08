from fastapi import HTTPException, Header
from middleware.constants import ACCESS_TOKEN


def validate_token(authorization: str = Header(...)):
    try:
        if authorization != ACCESS_TOKEN:
            raise HTTPException(status_code=401, detail="Invalid token")
        return authorization
    except HTTPException as error:
        raise error
    except:
        raise HTTPException(status_code=401, detail="Error validating token")
