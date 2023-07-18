from fastapi import HTTPException


class IDNotFoundException(HTTPException):

    def __init__(self, model, id: int) -> None:
        if id:
            super().__init__(
                status_code=404,
                detail=f'Model {model.__name__} with id {id} not found'
            )
            return
        super().__init__(
            status_code=404,
            detail=f'{model.__name__} id not found'
        )
