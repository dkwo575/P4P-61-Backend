# Function to update or add the building name by farm ID and building ID
def update_or_add_buildingName(data, farm_id, building_id, new_building_name):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    building["buildingName"] = new_building_name
                    return data  # Return the updated data structure
            # If building ID not found, add a new building
            farm["buildings"].append({
                "id": building_id,
                "buildingName": new_building_name,
                "events": [],
                "environment": [],
                "data": [],
                "plots": []
            })
            return data  # Return the updated data structure
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
    return data  # Return the updated data structure
