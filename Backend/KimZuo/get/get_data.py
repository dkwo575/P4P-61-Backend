# Function to update or add the data by farm ID, building ID, and data date
def get_Data(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            # Return data dict
                            return existing_data
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the area data by farm ID, building ID, and data date
def get_Area(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            area = existing_data["area"]
                            return area
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the fruitlets data by farm ID, building ID, and data date
def get_Fruitlets(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            fruitlets = existing_data["fruitlets"]
                            return fruitlets
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the height data by farm ID, building ID, and data date
def get_Height(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            height = existing_data["height"]
                            return height
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the leaves data by farm ID, building ID, and data date
def get_Leaves(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            leaves = existing_data["leaves"]
                            return leaves  # Return the updated data structure
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


# Function to update or add the width data by farm ID, building ID, and data date
def get_Width(data, farm_id, building_id, data_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for existing_data in building["data"]:
                        if existing_data["date"] == data_date:
                            width = existing_data["width"]
                            return width  # Return the updated data structure
                    # If environment date not found, return error
                    raise ValueError("Data Date not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")
