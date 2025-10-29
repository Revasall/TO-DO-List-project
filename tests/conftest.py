import pytest_asyncio, pytest
from datetime import datetime, timedelta
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from main import app
from app.database.models import Base, User, Task
from app.database.database import get_session
from app.security.security import get_password_hash
from app.security.limiter import limiter as app_limiter

SQLALCHEMY_DATABASE_URL = 'sqlite+aiosqlite:///:memory:?cache=shared'

engine_test = create_async_engine(SQLALCHEMY_DATABASE_URL, future=True )
TestingSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def session():
    async with TestingSessionLocal() as session:
        yield session

@pytest_asyncio.fixture
async def client(session):
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def disable_rate_limiter():
    """Disables the limiter for all tests."""
    app_limiter.enabled = False

@pytest_asyncio.fixture(scope='function')
async def test_user(session):
    """Create one test user for all tests"""
    user = User(
        username = 'test_user',
        email = 'test_user@example.com',
        hashed_password = get_password_hash('password')
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    yield user

    #Clear
    await session.delete(user)
    await session.commit()

@pytest_asyncio.fixture
async def auth_header(client, test_user):
    """Returns authorization headers with a valid access token."""
    responce = await client.post('/auth/login', data={
        'username': test_user.username,
        'password': 'password'
    })
    data = responce.json()
    token = data.get('access_token')
    yield ({'Authorization': f'Bearer {token}'} if token else {})

@pytest_asyncio.fixture(scope='function')
async def test_tasks_list(session, test_user):
    """Create test tasks for tests"""
    tasks_list = []

    for i in range(15):
        task = Task(
            title = f'task_{i}',
            description = f'test task number {i}',
            deadline = datetime.now() + timedelta(minutes=i),
            priority = i//5,
            owner_id = test_user.id
        )
        session.add(task)
        tasks_list.append(task)
    await session.commit()

    for task in tasks_list: 
        await session.refresh(task)

    yield tasks_list

    #Clear
    for task in tasks_list:
        await session.delete(task)
    await session.commit()

# Для запуска всех тестов проекта выполните команду:
# pytest
                
# Запустить тесты из конкретного файла:
# pytest tests/test_main.py
                  
# Остановиться на первом упавшем тесте:
# pytest -x
                  
# Перезапустить только упавшие тесты:
# pytest --lf
                  
# Запуск тестов, измененных с последнего коммита (если установлен pytest-xdist):
# pytest --last-failed
                  
# Запуск тестов с измерением времени выполнения:
# pytest --durations=5
                  
# Пропуск тестов с определенной меткой (например, медленных):
# pytest -m "not slow"