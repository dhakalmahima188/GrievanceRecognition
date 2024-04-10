from .models import IncrementalData
import pandas as pd
import os
from django.conf import settings

def export_data_for_training():
    # Check the count of IncrementalData objects
    if IncrementalData.objects.count() > 200:
        # Fetch the first 200 objects
        data_to_export = IncrementalData.objects.all()[:200]

        # Convert to DataFrame
        df1 = pd.DataFrame(list(data_to_export.values()))

        # Specify the file path for the CSV in the media folder
        csv_file_path = os.path.join(settings.MEDIA_ROOT, 'train.csv')
        
        # Export the DataFrame to CSV
        df1.to_csv(csv_file_path, index=False)
        print(f"Data exported to CSV at {csv_file_path}")

        # Training logic goes here (you mentioned to exclude this part)

        # After training, delete the objects that were exported
        data_to_export.delete()
        print("Exported data has been deleted from the database.")

        # Addit

def make_training():
    data=IncrementalData.objects.all()
    csv_file_path = os.path.join(settings.MEDIA_ROOT, 'new_data.csv')

    df1=pd.DataFrame(list(data.values()))
    df1.to_csv(csv_file_path, index=False)
    
    print(df1.head())
    df2=pd.read_csv(csv_file_path)
    print(df2.head())
    
    print("ok here")