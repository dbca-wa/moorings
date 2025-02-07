from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from tqdm import tqdm

COLUMN_MAPPINGS = []

class Command(BaseCommand):
    help = 'Import private moorings from file.'

    def handle(self, *args, **options):
        filepath = ""
        data=pd.read_csv(filepath, delimiter=',', dtype=str)

        data = self.data.rename(columns=COLUMN_MAPPINGS)
        data[data.columns] = data.apply(lambda x: x.str.strip() if isinstance(x, str) else x)
        data.fillna('', inplace=True)
        data.replace({np.nan: ''}, inplace=True)

        errors = []
        new = []
        updated = []

        for index, row in tqdm(data.iterrows(), total=data.shape[0]):
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