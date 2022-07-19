from fastapi import HTTPException, status

UnAuthorizedError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


AccessDeniedError = HTTPException(status_code=status.HTTP_403_FORBIDDEN)
