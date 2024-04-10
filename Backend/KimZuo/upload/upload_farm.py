# Function to update or add the farm name by ID
def update_or_add_farmName(data, farm_id, new_farm_name):
    for farm in data:
        if farm["id"] == farm_id:
            farm["farmName"] = new_farm_name
            return data
    # If farm ID not found, add a new farm
    data.append({
        "id": farm_id,
        "farmName": new_farm_name,
        "buildings": []
    })
    return data  # Return the updated data structure

