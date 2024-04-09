emissions_region = { #https://assets.publishing.service.gov.uk/media/64a677654dd8b3000c7fa545/2021-local-authority-ghg-emissions-stats-summary-update-060723.pdf
    #tonnes C02 per person (using per capita)
    'UK': 6500, #UK AVERAGE
    'ni': 10600, #NORTHERN IRELAND
    'scot': 7400, #SCOTLAND
    'wal': 9400, #WALES
    'ne': 6200, #NORTHERN ENGLAND
    'mid': 6300, #MIDLANDS ENGLAND
    'se': 5430, #SOUTHERN ENGLAND
    'london': 3400 #LONDON
}

conversion_factors = {
    #PRIVATE TRANSPORT: kg CO2 per km
    'private_transport_hybrid' : 0.06542, #Average hybrid electric car
    'private_transport_petrol' : 0.16323, #Average petrol car
    'private_transport_diesel' : 0.16815, #Average diesel  car
    'flight_mileage' : 0.2353, # Average passenger, mean of SH,LH,Domestic

    #UTILITIES: ELECTRICITY, HEATING, WATER: Average kg CO2 per kwh, gross cv
    'electricity' :  0.20496,
    'gas' : 0.18256, #heating for Natural Gas Boilers
    'oil' : 0.24557, #heating for Fuel Oil Boilers (Kerosene  aka burning oil) : most common
    'oilB' : 0.25359, #heating for Fuel Oil Boilers (Gas Oil)
    'water' : 0.177, # kg CO2e per m^3 used
    'water_per_person' : 54,  #average annual water usage per person, m3, https://www.statista.com/statistics/827267/average-household-water-usage-united-kingdom-uk/
    'waste_landfill' : 497.045, #kg CO2e per tonne of residual houeshold waste in landfill,
    'waste_per_person': 0.377, #tonnes #https://www.statista.com/statistics/322535/total-household-waste-volumes-in-england-uk-per-person/
    'recycling' :  21.281, #44.6% of arisings recycle

    #DIET, GOODS, SERVICES - KG CO2/£
    'general_grocery_shop' :  0.332,
    'meat_and_dairy' : 0.355,
    'goods_purchased' :  0.385,
    'services_purchased':  0.293

}

def categorise_income(income):
    #https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/bulletins/householddisposableincomeandinequality/financialyearending2022#glossary
    if income <= 14508:
        return "Very low"
    elif income <= 24249:
        return "Low"
    elif income <= 32349:
        return "Average"
    elif income <= 43490:
        return "Above Average"
    elif income <= 90000:
        return "High"
    else:
        return "Very High"

def footprint_regional_comparison():
    pass

def calculate_carbon_footprint(response, conversion_factors):

    # Calculate emission factors
    electricity_emission_factor = float(response.get('electricity')) * conversion_factors['electricity']
    heating_emission_factor = float(response.get('heating')) * conversion_factors[response.get('heatingType')]
    car_emission_factor = float(response.get('carMileage')) * conversion_factors[f'private_transport_{response.get('carType')}'] * 4.3
    flight_emission_factor = float(response.get('flight')) * conversion_factors['flight_mileage']
    meat_and_dairy_emission_factor = float(response.get('meatAndDairy')) * conversion_factors['meat_and_dairy'] * 4.3
    grocery_emission_factor = float(response.get('grocery')) * conversion_factors['general_grocery_shop'] * 4.3
    goods_emission_factor = float(response.get('goods')) * conversion_factors['goods_purchased'] * 4.3
    services_emission_factor = float(response.get('services')) * conversion_factors['services_purchased'] * 4.3
    waste_emission_factor = (conversion_factors['waste_per_person']/12) * conversion_factors['waste_landfill']
    water_emission_factor = (conversion_factors['water_per_person']/12) * conversion_factors['water']

    #User Information
    income_category = categorise_income(float(response.get('householdIncome')))
    household_size = float(response.get('householdSize'))
    recycling_status = str(response.get('recycling'))
    regional_average = emissions_region[f'{str(response.get('region'))}']
    uk_average = emissions_region['UK']

    # Calculate monthly carbon footprint = sum of emission factors (household footprint)/ household size -> individual footprint
    total_monthly_footprint = (sum([
        electricity_emission_factor,
        heating_emission_factor,
        car_emission_factor,
        flight_emission_factor,
        meat_and_dairy_emission_factor,
        grocery_emission_factor,
        goods_emission_factor,
        services_emission_factor,
        waste_emission_factor,
        water_emission_factor
    ])) / household_size

    # Calculate forecasted annual footprint = monthly footprint * 12 (estimation given current trends)
    annual_forecasted_footprint = total_monthly_footprint * 12

    # Save the emission factors and totals into a dictionary
    personal_profile = {
        'electricity_emission_factor': electricity_emission_factor,
        'heating_emission_factor': heating_emission_factor,
        'car_emission_factor': car_emission_factor,
        'flight_emission_factor': flight_emission_factor,
        'meat_and_dairy_emission_factor': meat_and_dairy_emission_factor,
        'grocery_emission_factor': grocery_emission_factor,
        'goods_emission_factor': goods_emission_factor,
        'services_emission_factor': services_emission_factor,
        'waste_emission_factor': waste_emission_factor,
        'water_emission_factor': water_emission_factor,

        'household_size': household_size,
        'income_category': income_category,
        'recycling_status': recycling_status,

        'total_carbon_footprint': total_monthly_footprint, #month
        'forecasted_annual_footprint': annual_forecasted_footprint, #month * 12
        'regional_annual_average_per_person': regional_average, #annual
        'UK_annual_average_per_person': uk_average
    }

    return personal_profile
