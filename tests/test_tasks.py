from datetime import datetime
import pytest
from sqlalchemy import delete, select

from app.database.models import Task
from app.security.security import decode_jwt_token

@pytest.mark.asyncio
async def test_create_task(client, auth_header, session):
    payload = {
            'title':'new_test_task',
            'description': '',
            'deadline': None,
            'priority' : 0
            }
    
    responce = await client.post('/user/tasks/', headers=auth_header, json=payload)
    assert responce.status_code in (200, 201)
    data = responce.json()
    assert data['title'] == payload['title'] and data['done'] is False
    # await session.execute(delete(Task).where(Task.id==data['id']))


@pytest.mark.asyncio
async def test_get_tasks_list_no_filter(client, auth_header, test_tasks_list):
    
    responce = await client.get('user/tasks/?page=1&limit=10&sort=id&sort_order=asc', headers=auth_header)
    assert responce.status_code == 200
    data = responce.json()
    print(data)
    assert isinstance(data, list) and len(data)==10

@pytest.mark.asyncio
async def test_get_tasks_list_filter_status(client, auth_header, test_user, test_tasks_list, session):
    done_task = Task(
        title=f"done_task",
        priority=1,
        done=True,
        owner_id=test_user.id
    )
    session.add(done_task)
    await session.commit()
    await session.refresh(done_task)

    responce = await client.get('user/tasks/?page=1&limit=10&status=true&sort=id&sort_order=asc', headers=auth_header)
    assert responce.status_code == 200
    data = responce.json()
    assert isinstance(data, list) and len(data)==1 
    assert data[0]['done'] == True

    responce = await client.get('user/tasks/?page=1&limit=10&status=false&sort=id&sort_order=asc', headers=auth_header)
    assert responce.status_code == 200
    data = responce.json()
    assert isinstance(data, list) and len(data)==10 
    assert all(data[i]['done'] == False for i in range(10))

@pytest.mark.asyncio
async def test_get_tasks_list_filter_prioryty(client, auth_header, test_tasks_list, session):
    
    for i in range(1,6):
        responce_filter = await client.get(f'/user/tasks/?page=1&limit=10&priority={i}&sort=id&sort_order=asc', headers=auth_header)
        assert responce_filter.status_code == 200
        data = responce_filter.json()
        assert isinstance(data, list)
        for task in data:
            task = await session.scalar(select(Task).where(Task.id == task['id']))
            assert task.priority == i
    



@pytest.mark.asyncio
async def test_get_one_task(client, auth_header, session):
    first_task = await session.scalar(select(Task).where(Task.id==1))

    responce = await client.get('/user/tasks/1', headers=auth_header)
    assert responce.status_code == 200
    data = responce.json()
    assert first_task.id == data['id']

@pytest.mark.asyncio
async def test_update_task_done(client, auth_header, session):
    first_task = await session.scalar(select(Task).where(Task.id==1))
   
    payload = {
        'title': None, 
        'description': None,
        'deadline': None,
        'done': True
    }

    responce = await client.put(f'/user/tasks/1', headers=auth_header, json=payload)
    assert responce.status_code==200, responce.text
    data = responce.json()
    assert data['title'] == first_task.title and data['id'] == first_task.id 
    assert data['done'] == True

@pytest.mark.asyncio
async def test_update_task_done(client, auth_header, session):
    first_task = await session.scalar(select(Task).where(Task.id==1))
   
    payload = {
        'title': 'update_name', 
        'description': 'update_desc',
        'deadline': str(datetime.now()),
        'done': None
    }

    responce = await client.put(f'/user/tasks/1', headers=auth_header, json=payload)
    assert responce.status_code==200, responce.text
    data = responce.json()
    assert data['title'] == payload['title'] and data['id'] == first_task.id 
    assert data['description'] == payload['description']
    assert data['done'] == False

@pytest.mark.asyncio
async def test_delete_task(client, auth_header, session):

    responce = await client.delete('/user/tasks/1', headers=auth_header)
    assert responce.status_code == 204

    first_task = await session.scalar(select(Task).where(Task.id==1))
    assert first_task is None