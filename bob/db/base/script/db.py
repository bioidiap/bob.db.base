"""The main entry for bob.db (click-based) scripts.

    This adds a ``db`` sub-command to the ``bob`` command.
"""
import click
import pkg_resources
from click_plugins import with_plugins
from bob.extension.scripts.click_helper import AliasedGroup

@with_plugins(pkg_resources.iter_entry_points('bob.db.cli'))
@click.group(cls=AliasedGroup)
def db():
    """Database management commands."""
    pass
