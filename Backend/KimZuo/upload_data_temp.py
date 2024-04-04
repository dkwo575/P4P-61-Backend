# Function to update or add the data by farm ID, building ID, and data date
def update_or_add_data(data, farm_id, building_id, data_date, new_data):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            existing_data.update(new_data)
                            return True
                    # If data date not found, add a new data entry
                    new_data_entry = {"date": data_date}
                    new_data_entry.update(new_data)
                    building["data"].append(new_data_entry)
                    return True
            # If building ID not found, add a new building with the data
            building_data = {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": 0,  # Assuming default values for other fields
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
                "plots": []
            }
            farm["buildings"].append(building_data)
            return True
    # If farm ID not found, add a new farm with the building and data
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": 0,  # Assuming default values for other fields
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
                "plots": []
            }
        ]
    })
    return True


# Function to update or add the area data by farm ID, building ID, and data date
def update_or_add_area(data, farm_id, building_id, data_date, new_area):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            existing_data["area"] = new_area
                            return True
                    # If data date not found, add a new data entry
                    new_data_entry = {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                    building["data"].append(new_data_entry)
                    return True
            # If building ID not found, add a new building with the data
            building_data = {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
                "plots": []
            }
            farm["buildings"].append(building_data)
            return True
    # If farm ID not found, add a new farm with the building and data
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
                "plots": []
            }
        ]
    })
    return True


# Function to update or add the area data by farm ID, building ID, and data date
def update_or_add_area(data, farm_id, building_id, data_date, new_area):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            existing_data["area"] = new_area
                            return True
                    # If data date not found, add a new data entry
                    new_data_entry = {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                    building["data"].append(new_data_entry)
                    return True
            # If building ID not found, add a new building with the data
            building_data = {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
                "plots": []
            }
            farm["buildings"].append(building_data)
            return True
    # If farm ID not found, add a new farm with the building and data
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [
                    {
                        "date": data_date,
                        "area": new_area,
                        "fruitlets": 0,  # Assuming default values for other fields
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }
                ],
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
