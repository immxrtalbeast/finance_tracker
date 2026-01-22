import json
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response, status

from application.dto.user import (
    UserByEmailDTO,
    UserCreateDTO,
    UserLoginDTO,
    UserResponseDTO,
)
from application.services.user_service import UserService
from presentation.api.dependencies import current_user_id, user_service

router = APIRouter(prefix="/users", tags=["Users🧑"])


@router.post("")
async def save_user(
    userDTO: UserCreateDTO, service: Annotated[UserService, Depends(user_service)]
):
    user_id = await service.save_user(
        email=userDTO.email, raw_password=userDTO.password
    )
    return {"user_id": user_id}


@router.post("/login")
async def login(
    dto: UserLoginDTO, service: Annotated[UserService, Depends(user_service)]
):
    token = await service.login(dto.email, dto.password)
    response = Response(
        json.dumps({"login": True}),
        media_type="application/json",
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        path="/",
    )
    return response


@router.get("/me", response_model=UserResponseDTO)
async def me(
    service: Annotated[UserService, Depends(user_service)],
    current_uid: Annotated[UUID, Depends(current_user_id)],
):
    user = await service.get_user_by_id(current_uid)
    return user


@router.get("/{user_id}", response_model=UserResponseDTO)
async def user(
    user_id: UUID,
    service: Annotated[UserService, Depends(user_service)],
    current_uid: Annotated[UUID, Depends(current_user_id)],
):
    if user_id != current_uid:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = await service.get_user_by_id(user_id)
    return user


@router.get("/email", response_model=UserResponseDTO, deprecated=True)
async def get_user_by_email(
    email: UserByEmailDTO,
    service: Annotated[UserService, Depends(user_service)],
):
    user = await service.get_user_by_email(email.email)
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: UUID,
    service: Annotated[UserService, Depends(user_service)],
    current_uid: Annotated[UUID, Depends(current_user_id)],
):
    if user_id != current_uid:
        raise HTTPException(status_code=403, detail="Forbidden")
    res = await service.delete(user_id)
    return {"status": res}
