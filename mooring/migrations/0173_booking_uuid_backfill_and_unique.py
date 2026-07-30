"""
Migration: backfill UUID values for existing Booking rows, then enforce
null=False and unique=True on the uuid field.

Why RunSQL instead of RunPython:
  With ~100k existing rows, a Python-level loop would be extremely slow and
  would hold a long transaction lock on the table. Using a single PostgreSQL
  UPDATE statement with gen_random_uuid() completes the entire backfill in
  a few seconds inside the database engine, with minimal locking overhead.

Operations (in order, within a single transaction):
  1. RunSQL  - populate uuid for any rows where uuid IS NULL
  2. AlterField - add NOT NULL and UNIQUE constraints once all rows have a value
"""

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mooring', '0172_booking_uuid_alter_booking_mooringarea_and_more'),
    ]

    operations = [
        # Step 1: backfill - assign a random UUID to every row that still has NULL.
        # gen_random_uuid() is a built-in PostgreSQL function (pgcrypto extension
        # is NOT required; it is available natively from PostgreSQL 13+).
        # The UPDATE is atomic and runs entirely inside the database engine.
        migrations.RunSQL(
            sql="""
                -- Pass 1: fill any remaining NULL uuids
                UPDATE mooring_booking
                SET uuid = gen_random_uuid()
                WHERE uuid IS NULL;

                -- Pass 2: resolve duplicate uuid values.
                -- In production each booking has its own uuid4() from Django, so
                -- this should be a no-op. In environments where rows were bulk-copied
                -- without regenerating the uuid column, this assigns a fresh
                -- gen_random_uuid() to every duplicate except the first occurrence
                -- (ordered by id, so the oldest record keeps its original value).
                WITH ranked AS (
                    SELECT id,
                           ROW_NUMBER() OVER (PARTITION BY uuid ORDER BY id) AS rn
                    FROM mooring_booking
                )
                UPDATE mooring_booking
                SET uuid = gen_random_uuid()
                WHERE id IN (SELECT id FROM ranked WHERE rn > 1);
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),

        # Step 2: tighten the column definition now that every row has a value.
        # AlterField translates to:
        #   ALTER COLUMN uuid SET NOT NULL
        #   ADD CONSTRAINT ... UNIQUE (uuid)
        migrations.AlterField(
            model_name='booking',
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
