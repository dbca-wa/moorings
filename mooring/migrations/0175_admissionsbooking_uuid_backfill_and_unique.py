"""
Migration: backfill UUID values for existing AdmissionsBooking rows, then enforce
null=False and unique=True on the uuid field.

Mirrors 0173_booking_uuid_backfill_and_unique.py (same strategy, different table).

Operations (in order, within a single transaction):
  1. RunSQL  - populate uuid for any rows where uuid IS NULL
  2. AlterField - add NOT NULL and UNIQUE constraints once all rows have a value
"""

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('mooring', '0174_admissionsbooking_uuid'),
    ]

    operations = [
        # Step 1: backfill - assign a random UUID to every row that still has NULL.
        # gen_random_uuid() is a built-in PostgreSQL function available natively
        # from PostgreSQL 13+.  The UPDATE runs entirely inside the database engine.
        migrations.RunSQL(
            sql="""
                -- Pass 1: fill any remaining NULL uuids
                UPDATE mooring_admissionsbooking
                SET uuid = gen_random_uuid()
                WHERE uuid IS NULL;

                -- Pass 2: resolve duplicate uuid values (should be a no-op in
                -- normal operation, but guards against bulk-copied rows).
                WITH ranked AS (
                    SELECT id,
                           ROW_NUMBER() OVER (PARTITION BY uuid ORDER BY id) AS rn
                    FROM mooring_admissionsbooking
                )
                UPDATE mooring_admissionsbooking
                SET uuid = gen_random_uuid()
                WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Step 2: tighten the column definition now that every row has a value.
        migrations.AlterField(
            model_name='admissionsbooking',
            name='uuid',
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                null=False,
                unique=True,
                db_index=True,
            ),
        ),
    ]
