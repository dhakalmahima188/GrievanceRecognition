from .models import IncrementalData
import pandas as pd

def make_training():
    data=IncrementalData.objects.all()
    df1=pd.DataFrame(list(data.values()))
    print(df1.head())
    
    print("ok here")