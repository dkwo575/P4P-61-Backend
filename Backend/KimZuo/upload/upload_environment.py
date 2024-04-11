# Function to update or add the environmental data by farm ID, building ID, environment date, and new environmental
# values
def update_or_add_environmentData(data, farm_id, building_id, environment_date, new_environment_data):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            # Update existing environmental data
                            environment.update(new_environment_data)
                            return data  # Return the updated data structure
                    # If environment date not found, add a new environment with the provided data
                    new_environment = {"date": environment_date}
                    new_environment.update(new_environment_data)
                    building["environment"].append(new_environment)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the environment
            new_environment = {"date": environment_date}
            new_environment.update(new_environment_data)
            building_data = {"id": building_id, "buildingName": "", "events": [], "environment": [new_environment],
                             "data": [], "plots": []}
            farm["buildings"].append(building_data)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and environment
    new_environment = {"date": environment_date}
    new_environment.update(new_environment_data)
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [new_environment],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure


# Function to update or add the temperature by farm ID, building ID, and environment date
def update_or_add_Temperature(data, farm_id, building_id, environment_date, new_temperature):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["temperature"] = new_temperature
                            return data  # Return the updated data structure
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": new_temperature,
                        "fluorescents": 0,  # Assuming default values for other fields
                        "co2Concentration": 0,
                        "irrigation": 0
                    })
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the environment
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": new_temperature,
                        "fluorescents": 0,  # Assuming default values for other fields
                        "co2Concentration": 0,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and environment
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": new_temperature,
                        "fluorescents": 0,  # Assuming default values for other fields
                        "co2Concentration": 0,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure


# Function to update or add the fluorescents by farm ID, building ID, and environment date
def update_or_add_Fluorescents(data, farm_id, building_id, environment_date, new_fluorescents):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["fluorescents"] = new_fluorescents
                            return data  # Return the updated data structure
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": new_fluorescents,
                        "co2Concentration": 0,
                        "irrigation": 0
                    })
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the environment
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": new_fluorescents,
                        "co2Concentration": 0,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and environment
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": new_fluorescents,
                        "co2Concentration": 0,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure


# Function to update or add the co2Concentration by farm ID, building ID, and environment date
def update_or_add_Co2Concentration(data, farm_id, building_id, environment_date, new_co2Concentration):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["co2Concentration"] = new_co2Concentration
                            return data  # Return the updated data structure
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": new_co2Concentration,
                        "irrigation": 0
                    })
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the environment
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": new_co2Concentration,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and environment
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": new_co2Concentration,
                        "irrigation": 0
                    }
                ],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure


# Function to update or add the irrigation by farm ID, building ID, and environment date
def update_or_add_Irrigation(data, farm_id, building_id, environment_date, new_irrigation):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["irrigation"] = new_irrigation
                            return data  # Return the updated data structure
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": 0,
                        "irrigation": new_irrigation
                    })
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the environment
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": 0,
                        "irrigation": new_irrigation
                    }
                ],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and environment
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [
                    {
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": 0,
                        "irrigation": new_irrigation
                    }
                ],
                "data": [],
                "plots": []
            }
        ]
    })
    return data  # Return the updated data structure
