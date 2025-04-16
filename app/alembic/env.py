from logging.config import fileConfig
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.db import Base
from app.models import user as user_model
from app.core.config import settings

# Alembic Config
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_online():
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        future=True,
    )

    async def do_run_migrations(connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            render_as_batch=True,
        )

        async with connection.begin():
            await context.run_migrations()

    import asyncio
    asyncio.run(do_run_migrations(connectable.connect()))