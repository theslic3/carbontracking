def calculateEnergyEmissions(electricity, gas, oil):
    return (electricity + gas) * 105 + oil * 113

def calculateTravelEmissions(car_mileage, longhaul, shorthaul):
    return car_mileage * 9.48 + shorthaul * 1100 + longhaul * 4400

#def calculateLifestylePurchaseEmissions(incomeBracket):

#def calculateGroceryEmissions():

def recyclingEmissions(newspaper, tin):
    return newspaper * 184 + tin * 166

def calculateFootprint(electricity, gas, oil, car_mileage, longhaul, shorthaul, newspaper, tin):
    total_energy_emissions = calculateEnergyEmissions(electricity, gas, oil)
    total_travel_emissions = calculateTravelEmissions(car_mileage, longhaul, shorthaul)
    total_recycling_emissions = recyclingEmissions(newspaper, tin)

    return total_energy_emissions + total_travel_emissions + total_recycling_emissions


def convertRecycling(factor):
    if (factor == "yes"):
        return 1
    else:
        return 0

def categoriseFootprint(footprint):
    if footprint < 10000:
        return "Very Low"
    elif 10000 <= footprint < 16000:
        return "Low"
    elif 16000 <= footprint < 22000:
        return "Medium"
    elif 22000 <= footprint < 30000:
        return "High"
    elif 30000 <= footprint < 50000:
        return "Very High"
    else:
        return "Extremely High"



#print("Carbon Footprint", calculateFootprint(23,45,75,325,2,7,1,0))
