from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np

COLUMN_MAPPINGS = {
    "Mooring Name": "name",
    "Mooring Park": "park",
    "Mooring Physical Type": "physical_type",
    "Mooring Class": "class",
    "Maximum Vessel Size (Metres)": "vessel_size",
    "Maximum Vessel Draft (Metres)": "vessel_draft",
    "Maximum Vessel Weight (Tonnes)": "vessel_weight",
}

class Command(BaseCommand):
    help = 'Import private moorings from file.'

    def handle(self, *args, **options):
        filepath = "tmp/test.csv"
        data=pd.read_csv(filepath, delimiter=',', dtype=str)

        data = data.rename(columns=COLUMN_MAPPINGS)
        data[data.columns] = data.apply(lambda x: x.str.strip() if isinstance(x, str) else x)
        data.fillna('', inplace=True)
        data.replace({np.nan: ''}, inplace=True)

        errors = []
        new = []
        updated = []

        for index, row in data.iterrows():
            try:
                pass
            except Exception as e:
                errors.append(e)

        print("New moorings added",len(new))
        print("Moorings updated", len(updated))

        if errors:
            print("\nErrors\n")
            for i in errors:
                print(i)