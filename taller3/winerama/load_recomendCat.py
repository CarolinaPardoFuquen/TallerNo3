import sys, os 
import pandas as pd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winerama.settings")

import django
django.setup()

from reviews.models import RecomendationsCat


def save_recomendation_from_row(recomendation_row):
    recomendation = RecomendationsCat()
    recomendation.ID_Restaurant2 = recomendation_row[0]
    recomendation.ID_User2 = recomendation_row[1]
    recomendation.name_Restaurant2 = recomendation_row[2]
    recomendation.Category = recomendation_row[4]
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

        print ("There are {} recomendations".format(RecomendationsCat.objects.count()))
        
    else:
        print ("Please, provide recomendation file path")
