# Function to get the farm name by ID
def get_farmName(data, farm_id):
    for farm in data:
        if farm["id"] == farm_id:
            farm_name = farm["farmName"]
            return farm_name
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")

