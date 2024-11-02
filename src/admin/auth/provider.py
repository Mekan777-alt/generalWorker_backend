from sqlalchemy.future import select
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider, AdminConfig, AdminUser
from starlette_admin.exceptions import LoginFailed

from database.session import async_session_maker
from models import Admin


class UsernameAndPasswordProvider(AuthProvider):

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        # Получаем пользователя из базы данных по логину (username)
        async with async_session_maker() as session:

            result = await session.execute(select(Admin).where(Admin.login == username))
            admin = result.scalar()

            # Если пользователь не найден, выбрасываем исключение
            if not admin or not admin.verify_password(password):
                raise LoginFailed("Invalid username or password")

            # Сохраняем логин пользователя в сессии
            request.session.update({"username": admin.login})
            return response

    async def is_authenticated(self, request: Request) -> bool:
        username = request.session.get("username", None)
        if username:
            async with async_session_maker() as session:
                result = await session.execute(select(Admin).where(Admin.login == username))
                admin = result.scalar()

                if admin:
                    # Сохраняем пользователя в состоянии request
                    request.state.user = admin
                    return True

        return False

    def get_admin_config(self, request: Request) -> AdminConfig:
        user = request.state.user  # Текущий пользователь
        return AdminConfig(
            app_title=f"Привет, {user.login}!",
        )

    def get_admin_user(self, request: Request) -> AdminUser:
        user = request.state.user  # Текущий пользователь
        return AdminUser(username=user.login)

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response
