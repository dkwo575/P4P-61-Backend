# Function to get the building name by farm ID and building ID
def get_buildingName(data, farm_id, building_id):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    building_name = building["buildingName"]
                    return building_name
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")
