"""TODO: Add description."""

# Import standard modules
from typing import Optional

# Import third-party modules
import click
from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import create_database, database_exists

# Import local modules
from . import db_config, Base

__author__ = "Vitali Lupusor"


@click.group()
def cli():
    """Command line interface for `data_model` module."""
    ...


@cli.command("init-db")
@click.option("--drivername", help="Driver/libraries to use for the database.")
@click.option("--username", help="Username to authenticate with the database.")
@click.option("--password", help="Password to authenticate with the database.")
@click.option("--host", help="The name of the host machine, i.e. IP or URL.")
@click.option("--port", help="The port on which to connect to the database.")
@click.option("--database", help="The name of the database.")
def init_db(
    drivername: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[int] = None,
    database: Optional[str] = None,
) -> None:
    """
    Initialise the tabales.

    Create the tables in the database according to the datamodel.

    Returns
        NoneType
    """
    # Configure database connection details
    db_config["drivername"] = drivername or db_config.get("drivername")
    db_config["username"] = username or db_config.get("username")
    db_config["password"] = password or db_config.get("password")
    db_config["host"] = host or db_config.get("host")
    db_config["port"] = port or db_config.get("port")
    db_config["database"] = database or db_config.get("database")

    # Build the connection string
    url = URL.create(**db_config)

    # Check whether database exists
    if not database_exists(url):
        click.echo("Creating the database...")
        create_database(url)
        click.echo(f'Database "{url.database}" created.')

    click.echo("Initialising the data model...")

    # Create database engine
    engine = create_engine(url)
    # Initialise tables
    Base.metadata.create_all(engine)

    click.echo("Done.")


if __name__ == "__main__":
    cli()
