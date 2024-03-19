import requests
from fractions import Fraction
import json

searchCocktailByName = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
searchIngredientByName = "https://www.thecocktaildb.com/api/json/v1/1/search.php?i="
lookupFullCocktailDetailsById = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php?i="

measurementsToMl = {   "oz" : 29.5735,
                       "cl" : 10,
                       "shot" : 44.3603,
                       "cup" :236.588,
                       "Oz" : 29.5735,
                       "Cl" : 10,
                       "Shot" : 44.3603,
                       "Cup" :236.588
                   }

gender = {
            "Male" : 0.68,
            "Female" : 0.55
        }

def GetIngredient(ingredientName):
    drinkToSearch = searchIngredientByName + ingredientName
    response = json.loads(requests.get(drinkToSearch).text)
    return response

def GetAlcoholName(alcoholName):
    drinkToSearch = searchCocktailByName + alcoholName
    response = json.loads(requests.get(drinkToSearch).text)
    return response

def GetAlcoholById(alcoholId):
    drinkToSearch = lookupFullCocktailDetailsById + alcoholId
    response = json.loads(requests.get(drinkToSearch).text)
    return response

def DrinkVolume(alcoholId):
    
    drinkName = GetAlcoholById(alcoholId)
    drinkName = drinkName["drinks"][0]
    
    glassVolume = 0
    
    alcoholLevel = 0
    alcoholPecentage = 0
    
    counter = 1
    
    while drinkName["strIngredient" + str(counter)] is not None:
        
        ingredientName = drinkName["strIngredient" + str(counter)]
        ingredientName = GetIngredient(ingredientName)
        ingredientName = ingredientName["ingredients"][0]

        if ingredientName["strABV"] is not None:
            ingredientName = int(ingredientName["strABV"])
            alcoholPecentage = ingredientName

        if drinkName["strMeasure" + str(counter)] is not None:    
            volumeComposition = drinkName["strMeasure" + str(counter)].strip()
            volumeComposition = volumeComposition.split(" ")
            try:
                volumeComposition = float(Fraction(volumeComposition[0])) * measurementsToMl[volumeComposition[len(volumeComposition)-1]]
            except:
                counter += 1
                alcoholPecentage = 0
                volumeComposition = 0
                continue

            alcoholLevel += alcoholPecentage/100 * volumeComposition
            glassVolume += volumeComposition

        counter += 1
        alcoholPecentage = 0
        volumeComposition = 0
    
    return glassVolume,alcoholLevel

def DrinksAbvLevel(glassVolume,alcoholLevel):
    if glassVolume == 0:
        glassVolume = 1
    abv = round(alcoholLevel/glassVolume,2) * 100
    return abv
    
#glassVolume,alcoholLevel = DrinkVolume("11007")
#DrinksAbvLevel(glassVolume,alcoholLevel)

def BloodAlcoholConcentration(weight,alcoholLevel,customerGender,timePassedInHours):
    weight = weight * 1000
    widmarkFactor = gender[customerGender]
    Bac = round((alcoholLevel/((weight * widmarkFactor)-(timePassedInHours * 0.015))) * 100,4)
    return Bac
    
#BloodAlcoholConcentration(54,56,"female",5)

def BacLevels(bac):
    if bac > 0.1:
        return True
    else:
        return False