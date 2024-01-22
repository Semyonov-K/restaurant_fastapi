from http import HTTPStatus

from typing import Union, Optional
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from restaurant_app.core.db import get_async_session
from restaurant_app.crud.restaurant import create_entity, read_all_entity, get_entity_by_id, update_entity, delete_entity
from restaurant_app.schemas.restaurant import SubMenuCRU, DishCRU

router = APIRouter()


async def create_api_new_entity(
        new: Union[SubMenuCRU, DishCRU],
        type_of_entity: str,
        id_sm: Optional[int],
        session: AsyncSession
):
    try:
        new_ent = await create_entity(new, type_of_entity, id_sm, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f'Такое название {type_of_entity} уже существует!'
        )
    return new_ent


async def get_api_all_entity(
        type_of_entity: str,
        session: AsyncSession
):
    all_ent = await read_all_entity(type_of_entity, session)
    return all_ent


async def update_api_entity(
        entity_id: int,
        type_of_entity: str,
        obj_in: Union[SubMenuCRU, DishCRU],
        session: AsyncSession
):
    ent = await get_entity_by_id(entity_id, type_of_entity, session)
    if ent is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Меню не найдено!'
        )
    try:
        ent = await update_entity(ent, obj_in, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название меню уже существует!'
        )
    return ent


async def remove_api_entity(
        entity_id: int,
        type_of_entity: str,
        session: AsyncSession
):
    ent = get_entity_by_id(entity_id, type_of_entity, session)
    try:
        ent = await delete_entity(
            ent, session
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого меню не существует!'
        )
    return ent


@router.post('/menus/')
async def create_new_main_menu(
    menu: SubMenuCRU,
    session: AsyncSession = Depends(get_async_session)
):
    return create_api_new_entity(menu, 'menu', session)


@router.post('/menus/{api_test_menu_id}/submenus')
async def create_new_main_menu(
    submenu: SubMenuCRU,
    api_test_menu_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return create_api_new_entity(submenu, 'submenu', api_test_menu_id, session)


@router.post('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
async def create_new_main_menu(
    dish: DishCRU,
    api_test_menu_id: int,
    api_test_submenu_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return create_api_new_entity(dish, 'dish', api_test_submenu_id, session)


@router.get('/menus/')
async def get_menus(
    session: AsyncSession = Depends(get_async_session)
):
    return read_all_entity('menu', session)


@router.get('/menus/{api_test_menu_id}/submenus')
async def get_submenus(
    session: AsyncSession = Depends(get_async_session)
):
    return read_all_entity('submenu', session)


@router.get('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes')
async def get_dishes(
    session: AsyncSession = Depends(get_async_session)
):
    return read_all_entity('dish', session)


@router.get('/menus/{api_test_menu_id}')
async def get_menu(
    api_test_menu_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return get_entity_by_id(api_test_menu_id, 'menu', session)


@router.get('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
async def get_submenu(
    api_test_submenu_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return get_entity_by_id(api_test_submenu_id, 'submenu', session)


@router.get('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
async def get_dish(
    api_test_dish_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    return get_entity_by_id(api_test_dish_id, 'dish', session)


@router.delete('/menus/{api_test_menu_id}')
async def remove_menu(
        api_test_menu_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    menu = get_entity_by_id(api_test_menu_id, 'menu', session)
    try:
        menu = await delete_entity(
            menu, session
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого меню не существует!'
        )
    return menu


@router.delete('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
async def remove_submenu(
        api_test_submenu_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = get_entity_by_id(api_test_submenu_id, 'submenu', session)
    try:
        submenu = await delete_entity(
            submenu, session
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого подменю не существует!'
        )
    return submenu


@router.delete('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
async def remove_dish(
        api_test_dish_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    dish = get_entity_by_id(api_test_dish_id, 'dish', session)
    try:
        dish = await delete_entity(
            dish, session
        )
    except:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Такого блюда не существует!'
        )
    return dish


@router.patch('/menus/{api_test_menu_id}')
async def update_menu(
        api_test_menu_id: int,
        obj_in: SubMenuCRU,
        session: AsyncSession = Depends(get_async_session),
):
    menu = await get_entity_by_id(api_test_menu_id, 'menu', session)
    if menu is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Меню не найдено!'
        )
    try:
        menu = await update_entity(menu, obj_in, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название меню уже существует!'
        )
    return menu


@router.patch('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}')
async def update_submenu(
        api_test_submenu_id: int,
        obj_in: SubMenuCRU,
        session: AsyncSession = Depends(get_async_session),
):
    submenu = await get_entity_by_id(api_test_submenu_id, 'submenu', session)
    if submenu is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Подменю не найдено!'
        )
    try:
        submenu = await update_entity(submenu, obj_in, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название подменю уже существует!'
        )
    return submenu


@router.patch('/menus/{api_test_menu_id}/submenus/{api_test_submenu_id}/dishes/{api_test_dish_id}')
async def update_dish(
        api_test_dish_id: int,
        obj_in: DishCRU,
        session: AsyncSession = Depends(get_async_session),
):
    dish = await get_entity_by_id(api_test_dish_id, 'dish', session)
    if dish is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, 
            detail='Блюдо не найдено!'
        )
    try:
        dish = await update_entity(dish, obj_in, session)
    except:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Такое название блюдо уже существует!'
        )
    return dish

# @router.post('/menus/')
# async def create_new_main_menu(
#         menu: MenuCreate,
#         session: AsyncSession = Depends(get_async_session)
# ):
#     try:
#         new_menu = await create_menu(menu, session)
#     except:
#         raise HTTPException(
#             status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
#             detail='Такое название меню уже существует!'
#         )
#     return new_menu


# @router.get('/menus/')
# async def get_all_meeting_rooms(
#         session: AsyncSession = Depends(get_async_session),
# ):
#     all_rooms = await read_all_menus(session)
#     return all_rooms 


# @router.patch('/{api_test_menu_id}',)
# async def update_menu(
#         menu_id: int,
#         obj_in: MenuCreate,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     menu = await get_menu_by_id(menu_id, session)
#     if menu is None:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, 
#             detail='Меню не найдено!'
#         )
#     try:
#         menu = await update_menu(menu, obj_in, session)
#     except:
#         raise HTTPException(
#             status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
#             detail='Такое название меню уже существует!'
#         )
#     return menu



# @router.delete('/{api_test_menu_id}')
# async def remove_menu(
#         menu_id: int,
#         session: AsyncSession = Depends(get_async_session),
# ):
#     menu = get_menu_by_id(menu_id, session)
#     try:
#         menu = await delete_menu(
#             menu, session
#         )
#     except:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='Такого меню не существует!'
#         )
#     return menu
