# Function to update or add the environmental data by farm ID, building ID, environment date, and new environmental
# values
def get_environmentData(data, farm_id, building_id, environment_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            # Return environment dict
                            return environment
                    # If environment date not found, return error
                    raise ValueError("Environment Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the temperature by farm ID, building ID, and environment date
def get_Temperature(data, farm_id, building_id, environment_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            temperature = environment["temperature"]
                            return temperature
                    # If environment date not found, return error
                    raise ValueError("Environment Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the fluorescents by farm ID, building ID, and environment date
def get_Fluorescents(data, farm_id, building_id, environment_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            fluorescents = environment["fluorescents"]
                            return fluorescents
                    # If environment date not found, return error
                    raise ValueError("Environment Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the co2Concentration by farm ID, building ID, and environment date
def get_Co2Concentration(data, farm_id, building_id, environment_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            co2Concentration = environment["co2Concentration"]
                            return co2Concentration
                    # If environment date not found, return error
                    raise ValueError("Environment Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the irrigation by farm ID, building ID, and environment date
def get_Irrigation(data, farm_id, building_id, environment_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            irrigation = environment["irrigation"]
                            return irrigation
                    # If environment date not found, return error
                    raise ValueError("Environment Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")

