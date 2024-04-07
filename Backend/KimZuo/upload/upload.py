import json
import os


# Function to update or add the farm name by ID
def update_or_add_farm_name(data, farm_id, new_farm_name):
    for farm in data:
        if farm["id"] == farm_id:
            farm["farmName"] = new_farm_name
            return True
    # If farm ID not found, add a new farm
    data.append({
        "id": farm_id,
        "farmName": new_farm_name,
        "buildings": []
    })
    return True


# Function to update or add the building name by farm ID and building ID
def update_or_add_building_name(data, farm_id, building_id, new_building_name):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    building["buildingName"] = new_building_name
                    return True
            # If building ID not found, add a new building
            farm["buildings"].append({
                "id": building_id,
                "buildingName": new_building_name,
                "events": [],
                "environment": [],
                "data": [],
                "plots": []
            })
            return True
    # If farm ID not found, add a new farm with the building
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": new_building_name,
                "events": [],
                "environment": [],
                "data": [],
                "plots": []
            }
        ]
    })
    return True


# Function to update or add the event text by farm ID, building ID, and event date
def update_or_add_event_text(data, farm_id, building_id, event_date, new_text):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for event in building["events"]:
                        if event["date"] == event_date:
                            event["text"] = new_text
                            return True
                    # If event date not found, add a new event
                    building["events"].append({
                        "date": event_date,
                        "text": new_text
                    })
                    return True
            # If building ID not found, add a new building with the event
            farm["buildings"].append({
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [
                    {
                        "date": event_date,
                        "text": new_text
                    }
                ],
                "environment": [],
                "data": [],
                "plots": []
            })
            return True
    # If farm ID not found, add a new farm with the building and event
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [
                    {
                        "date": event_date,
                        "text": new_text
                    }
                ],
                "environment": [],
                "data": [],
                "plots": []
            }
        ]
    })
    return True


# Function to update or add the environmental data by farm ID, building ID, environment date, and new environmental
# values
def update_or_add_environment_data(data, farm_id, building_id, environment_date, new_environment_data):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            # Update existing environmental data
                            environment.update(new_environment_data)
                            return True
                    # If environment date not found, add a new environment with the provided data
                    new_environment = {"date": environment_date}
                    new_environment.update(new_environment_data)
                    building["environment"].append(new_environment)
                    return True
            # If building ID not found, add a new building with the environment
            new_environment = {"date": environment_date}
            new_environment.update(new_environment_data)
            building_data = {"id": building_id, "buildingName": "", "events": [], "environment": [new_environment],
                             "data": [], "plots": []}
            farm["buildings"].append(building_data)
            return True
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
    return True


# Function to update or add the temperature by farm ID, building ID, and environment date
def update_or_add_temperature(data, farm_id, building_id, environment_date, new_temperature):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["temperature"] = new_temperature
                            return True
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": new_temperature,
                        "fluorescents": 0,  # Assuming default values for other fields
                        "co2Concentration": 0,
                        "irrigation": 0
                    })
                    return True
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
            return True
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
    return True


# Function to update or add the fluorescents by farm ID, building ID, and environment date
def update_or_add_fluorescents(data, farm_id, building_id, environment_date, new_fluorescents):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["fluorescents"] = new_fluorescents
                            return True
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": new_fluorescents,
                        "co2Concentration": 0,
                        "irrigation": 0
                    })
                    return True
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
            return True
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
    return True


# Function to update or add the co2Concentration by farm ID, building ID, and environment date
def update_or_add_co2Concentration(data, farm_id, building_id, environment_date, new_co2Concentration):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["co2Concentration"] = new_co2Concentration
                            return True
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": new_co2Concentration,
                        "irrigation": 0
                    })
                    return True
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
            return True
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
    return True


# Function to update or add the irrigation by farm ID, building ID, and environment date
def update_or_add_irrigation(data, farm_id, building_id, environment_date, new_irrigation):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for environment in building["environment"]:
                        if environment["date"] == environment_date:
                            environment["irrigation"] = new_irrigation
                            return True
                    # If environment date not found, add a new environment
                    building["environment"].append({
                        "date": environment_date,
                        "temperature": 0,  # Assuming default values for other fields
                        "fluorescents": 0,
                        "co2Concentration": 0,
                        "irrigation": new_irrigation
                    })
                    return True
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
            return True
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
    return True


# # Path to the database file
# database_path = os.path.join(os.getcwd(), "database", "farm_data.json")
# new_database_path = os.path.join(os.getcwd(), "database", "new_new_farm_data.json")
#
# # Load data from JSON file
# with open(database_path, "r") as infile:
#     data = json.load(infile)
#
# # Example usage:
# # Update farm name with ID 0
# if update_or_add_farm_name(data, 1, "Farm 2"):
#     print("Farm name updated successfully")
# else:
#     print("Failed to update farm name")
#
# # Update building name with farm ID 0 and building ID 0
# if update_or_add_building_name(data, 0, 0, "New Building Name"):
#     print("Building name updated successfully")
# else:
#     print("Failed to update building name")
#
# # Update event text with farm ID 0, building ID 0, and event date "2023-07-10"
# if update_or_add_event_text(data, 0, 0, "2023-07-10", "New Event Text"):
#     print("Event text updated successfully")
# else:
#     print("Failed to update event text")
#
# # Update temperature with farm ID 0, building ID 0, and environment date "2023-03-12"
# if update_or_add_temperature(data, 0, 0, "2023-03-12", 25.0):
#     print("Temperature updated successfully")
# else:
#     print("Failed to update temperature")
#
# # Write updated data back to the JSON file
# with open(new_database_path, "w") as outfile:
#     json.dump(data, outfile, indent=4)
