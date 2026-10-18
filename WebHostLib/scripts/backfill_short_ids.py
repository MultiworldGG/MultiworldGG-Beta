"""
Backfill short_id values for all rooms that don't have one.

Phase 2b of the route migration. Once Phase 2a has been deployed and is
populating short_ids for new rooms, this script catches up the rooms
that existed before. Idempotent and safe to re-run.

Wire up as a Flask CLI command in your app factory:

    from WebHostLib.scripts.backfill_short_ids import register_cli
    register_cli(app)

Then run:

    flask --app WebHostLib backfill-short-ids
    flask --app WebHostLib backfill-short-ids --dry-run
    flask --app WebHostLib backfill-short-ids --batch-size 50
"""

import logging
import sys

import click
from flask.cli import with_appcontext

from WebHostLib.short_id import assign_short_id, ShortIDExhaustedError

logger = logging.getLogger(__name__)


def backfill(batch_size: int = 100, dry_run: bool = False) -> dict:
    """Backfill short_id for all rooms where it is NULL.

    Args:
        batch_size: How many rooms to assign before committing the
            transaction. Smaller batches = more frequent commits = less
            risk of a long-running transaction, but more DB roundtrips.
        dry_run: If True, calculate what would change but don't commit.

    Returns:
        Stats dict: ``{"total": int, "assigned": int, "failed": int}``
    """
    # Local imports so this module can be tested without spinning up
    # the full WebHostLib environment.
    from sqlalchemy import select  # noqa: WPS433
    from WebHostLib.models import db, Room  # noqa: WPS433

    rooms_without = db.session.scalars(
        select(Room).where(Room.short_id.is_(None))
    ).all()
    total = len(rooms_without)
    logger.info("Backfilling short_id for %d rooms (dry_run=%s)", total, dry_run)

    assigned = 0
    failed = 0

    for index, room in enumerate(rooms_without, start=1):
        try:
            assign_short_id(db.session, room)
            assigned += 1
        except ShortIDExhaustedError:
            logger.exception("Could not assign short_id to room %s", room.id)
            failed += 1
            db.session.rollback()
            continue

        if assigned % batch_size == 0:
            if not dry_run:
                db.session.commit()
            logger.info("Progress: %d / %d (failed: %d)", assigned, total, failed)

    # Final batch
    if not dry_run:
        db.session.commit()
    else:
        db.session.rollback()

    logger.info(
        "Done. assigned=%d failed=%d total=%d dry_run=%s",
        assigned, failed, total, dry_run,
    )
    return {"total": total, "assigned": assigned, "failed": failed}


# ---------------------------------------------------------------------------
# Flask CLI wiring
# ---------------------------------------------------------------------------

@click.command("backfill-short-ids")
@click.option("--batch-size", default=100, type=int,
              help="Rooms per transaction commit. Default 100.")
@click.option("--dry-run", is_flag=True,
              help="Calculate but don't persist changes.")
@with_appcontext
def backfill_short_ids_command(batch_size, dry_run):
    """Assign short_id to every room that doesn't have one."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    stats = backfill(batch_size=batch_size, dry_run=dry_run)

    click.echo(f"Backfill complete:")
    click.echo(f"  Total rooms without short_id: {stats['total']}")
    click.echo(f"  Successfully assigned:        {stats['assigned']}")
    click.echo(f"  Failed:                       {stats['failed']}")

    if dry_run:
        click.echo("(dry-run: no changes persisted)")
    if stats["failed"] > 0:
        sys.exit(1)


def register_cli(app):
    """Register the backfill command with a Flask app's CLI."""
    app.cli.add_command(backfill_short_ids_command)
