from starlette.applications import Starlette
from database.session import engine
from starlette_admin.contrib.sqla import Admin
from starlette_admin import I18nConfig
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
from admin.auth.provider import UsernameAndPasswordProvider

i18n_config = I18nConfig(default_locale="ru")

app = Starlette()

admin = Admin(engine,
              title="generalWorkers ADMIN",
              base_url="/admin",
              auth_provider=UsernameAndPasswordProvider(),
              middlewares=[Middleware(SessionMiddleware, secret_key='secret')],
              i18n_config=i18n_config
              )


admin.mount_to(app)
