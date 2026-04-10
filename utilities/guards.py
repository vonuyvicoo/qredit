from fastapi import Depends

from utilities.jwtUtils import validate_token

AuthGuard = Depends(validate_token)
