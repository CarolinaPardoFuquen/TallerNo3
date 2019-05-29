import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import Recomendations


def save_recomendation_from_row(recomendation_row):
    recomendation = Recomendations()
    #recomendation.ID_Restaurant = recomendation_row[0]
    recomendation.ID_User = recomendation_row[3]
    recomendation.name_Restaurant = recomendation_row[1]
    recomendation.City = recomendation_row[2]
    recomendation.save()
    
    
if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        print ("Reading from file " + str(sys.argv[1]))
        recomendations_df = pd.read_csv(sys.argv[1])
        print (recomendations_df)

        recomendations_df.apply(
            save_recomendation_from_row,
            axis=1
        )

        print ("There are {} recomendations".format(Recomendations.objects.count()))
        
    else:
        print ("Please, provide recomendation file path")
