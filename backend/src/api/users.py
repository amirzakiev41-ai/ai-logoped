from fastapi import APIRouter, Request

from schemas.user_schemas import CreateUserRequest, UserResponse, UpdateUserRequest, AllUsersResponse, MessageResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/auth/register_user", response_model=UserResponse)
def register_user(request: Request, body: CreateUserRequest) -> UserResponse:
    container = request.app.state.container
    
    return container.user_service.register_user(body.user_name,
                                                body.email)

@router.post("/auth/create_user", response_model=UserResponse)
def create_user(request: Request, body: CreateUserRequest) -> UserResponse:
    container = request.app.state.container
    
    return container.user_service.create_user(body.user_name,
                                              body.email)

@router.get("/all_users", response_model=AllUsersResponse)
def get_all_users(request: Request):
    container = request.app.state.container

    return AllUsersResponse(all_users=container.user_service.get_all_users())

@router.get("/all_users/{user_id}", response_model=UserResponse)
def get_user_by_id(request: Request, user_id: int) -> UserResponse:
    container = request.app.state.container
    
    return container.user_service.get_user_by_id(user_id)

@router.patch("/{user_id}", response_model=MessageResponse)
def update_user_name(request: Request, user_id: int, body: UpdateUserRequest) -> MessageResponse:
    container = request.app.state.container
    
    container.user_service.update_user_name(user_id=user_id,
                                            user_name=body.user_name)
    
    return MessageResponse(
        message="Имя пользователя успешно изменено."
    )

@router.delete("/{user_id}", response_model=MessageResponse)
def delete_user(request: Request, user_id: int) -> MessageResponse:
    container = request.app.state.container
    
    container.user_service.delete_user(user_id=user_id)

    return MessageResponse(
    message="Пользователь успешно удалён."
    )