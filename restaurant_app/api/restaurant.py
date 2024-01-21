from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from restaurant_app.core.db import get_async_session
from restaurant_app.crud.restaurant import create_menu, read_all_menus, get_menu_by_id, update_menu, delete_menu
from restaurant_app.schemas.restaurant import MenuCreate

router = APIRouter()


@router.post('/menus/')
async def create_new_main_menu(
        menu: MenuCreate,
        session: AsyncSession = Depends(get_async_session)
):
    try:
        new_menu = await create_menu(menu, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название меню уже существует!'
        )
    return new_menu


@router.get('/menus/')
async def get_all_meeting_rooms(
        session: AsyncSession = Depends(get_async_session),
):
    all_rooms = await read_all_menus(session)
    return all_rooms 


@router.patch('/{api_test_menu_id}',)
async def update_menu(
        menu_id: int,
        obj_in: MenuCreate,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await get_menu_by_id(menu_id, session)
    if menu is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Меню не найдено!'
        )
    try:
        menu = await update_menu(menu, obj_in, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название меню уже существует!'
        )
    return menu



@router.delete('/{api_test_menu_id}')
async def remove_menu(
        menu_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    menu = get_menu_by_id(menu_id, session)
    try:
        menu = await delete_menu(
            menu, session
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого меню не существует!'
        )
    return menu
