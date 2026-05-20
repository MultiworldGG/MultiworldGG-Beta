import click
from flask.cli import AppGroup
from sqlalchemy import select, func

from Utils import format_SI_prefix

stats_cli = AppGroup("stats")


@stats_cli.command("show")
def show() -> None:
    from WebHostLib.models import GameDataPackage, db

    total_games_package_count: int = 0
    total_games_package_size: int = 0
    top_10_package_sizes: list[tuple[int, str]] = []

    total_games_package_count = db.session.scalar(
        select(func.count()).select_from(GameDataPackage)
    ) or 0
    total_games_package_size = db.session.scalar(
        select(func.sum(func.length(GameDataPackage.data)))
    ) or 0
    top_10_package_sizes = list(db.session.execute(
        select(func.length(GameDataPackage.data), GameDataPackage.checksum)
        .order_by(func.length(GameDataPackage.data).desc())
        .limit(10)
    ).all())

    click.echo(f"Total number of games packages: {total_games_package_count}")
    click.echo(f"Total size of games packages:   {format_SI_prefix(total_games_package_size, power=1024)}B")
    click.echo(f"Top {len(top_10_package_sizes)} biggest games packages:")
    for size, checksum in top_10_package_sizes:
        click.echo(f"    {checksum}: {size:>8d}")
