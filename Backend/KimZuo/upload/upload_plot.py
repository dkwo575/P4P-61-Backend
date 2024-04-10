def update_or_add_plot_data(data, farm_id, building_id, plot_id, new_plot_data):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            # If plot data for the date not found, add a new data entry
                            plot.update(new_plot_data)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {"id": plot_id}
                    new_plot.update(new_plot_data)
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [new_plot_data]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [new_plot_data]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotName(data, farm_id, building_id, plot_id, new_plotName):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            plot["plotName"] = new_plotName
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the provided data
                    building["plots"].append({
                        "id": plot_id,
                        "plotName": new_plotName
                    })
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot
            building_data = {
                "id": building_id,
                "buildingName": "",
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": new_plotName
                }]
            }
            farm["buildings"].append(building_data)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building and plot
    new_building = {
        "id": building_id,
        "buildingName": "",
        "events": [],
        "environment": [],
        "data": [],
        "plots": [{
            "id": plot_id,
            "plotName": new_plotName
        }]
    }
    data.append({
        "id": farm_id,
        "farmName": "",
        "buildings": [new_building]
    })
    return data  # Return the updated data structure


def update_or_add_plotArea(data, farm_id, building_id, plot_id, plot_date, new_plot_area):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["area"] = new_plot_area
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": new_plot_area,
                                "fruitlets": 0,
                                "height": 0,
                                "leaves": 0,
                                "volume": 0,
                                "width": 0
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": new_plot_area,
                            "fruitlets": 0,
                            "height": 0,
                            "leaves": 0,
                            "volume": 0,
                            "width": 0
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": new_plot_area,
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": new_plot_area,
                    "fruitlets": 0,
                    "height": 0,
                    "leaves": 0,
                    "volume": 0,
                    "width": 0
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotFruitlets(data, farm_id, building_id, plot_id, plot_date, new_plot_fruitlets):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["fruitlets"] = new_plot_fruitlets
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": 0,
                                "fruitlets": new_plot_fruitlets,
                                "height": 0,
                                "leaves": 0,
                                "volume": 0,
                                "width": 0
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": 0,
                            "fruitlets": new_plot_fruitlets,
                            "height": 0,
                            "leaves": 0,
                            "volume": 0,
                            "width": 0
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": 0,
                        "fruitlets": new_plot_fruitlets,
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": 0,
                    "fruitlets": new_plot_fruitlets,
                    "height": 0,
                    "leaves": 0,
                    "volume": 0,
                    "width": 0
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotHeight(data, farm_id, building_id, plot_id, plot_date, new_plot_height):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["height"] = new_plot_height
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": 0,
                                "fruitlets": 0,
                                "height": new_plot_height,
                                "leaves": 0,
                                "volume": 0,
                                "width": 0
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": 0,
                            "fruitlets": 0,
                            "height": new_plot_height,
                            "leaves": 0,
                            "volume": 0,
                            "width": 0
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": 0,
                        "fruitlets": 0,
                        "height": new_plot_height,
                        "leaves": 0,
                        "volume": 0,
                        "width": 0
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": 0,
                    "fruitlets": 0,
                    "height": new_plot_height,
                    "leaves": 0,
                    "volume": 0,
                    "width": 0
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotLeaves(data, farm_id, building_id, plot_id, plot_date, new_plot_leaves):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["leaves"] = new_plot_leaves
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": 0,
                                "fruitlets": 0,
                                "height": 0,
                                "leaves": new_plot_leaves,
                                "volume": 0,
                                "width": 0
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": 0,
                            "fruitlets": 0,
                            "height": 0,
                            "leaves": new_plot_leaves,
                            "volume": 0,
                            "width": 0
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": 0,
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": new_plot_leaves,
                        "volume": 0,
                        "width": 0
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": 0,
                    "fruitlets": 0,
                    "height": 0,
                    "leaves": new_plot_leaves,
                    "volume": 0,
                    "width": 0
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotVolume(data, farm_id, building_id, plot_id, plot_date, new_plot_volume):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["volume"] = new_plot_volume
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": 0,
                                "fruitlets": 0,
                                "height": 0,
                                "leaves": 0,
                                "volume": new_plot_volume,
                                "width": 0
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": 0,
                            "fruitlets": 0,
                            "height": 0,
                            "leaves": 0,
                            "volume": new_plot_volume,
                            "width": 0
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": 0,
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": 0,
                        "volume": new_plot_volume,
                        "width": 0
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": 0,
                    "fruitlets": 0,
                    "height": 0,
                    "leaves": 0,
                    "volume": new_plot_volume,
                    "width": 0
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure


def update_or_add_plotWidth(data, farm_id, building_id, plot_id, plot_date, new_plot_width):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    existing_data["width"] = new_plot_width
                                    return data  # Return the updated data structure
                            # If plot data for the date not found, add a new data entry
                            new_data_entry = {
                                "date": plot_date,
                                "area": 0,
                                "fruitlets": 0,
                                "height": 0,
                                "leaves": 0,
                                "volume": 0,
                                "width": new_plot_width
                            }
                            plot["data"].append(new_data_entry)
                            return data  # Return the updated data structure
                    # If plot ID not found, add a new plot with the data
                    new_plot = {
                        "id": plot_id,
                        "plotName": "",  # Assuming default plot name
                        "data": [{
                            "date": plot_date,
                            "area": 0,
                            "fruitlets": 0,
                            "height": 0,
                            "leaves": 0,
                            "volume": 0,
                            "width": new_plot_width
                        }]
                    }
                    building["plots"].append(new_plot)
                    return data  # Return the updated data structure
            # If building ID not found, add a new building with the plot and data
            new_building = {
                "id": building_id,
                "buildingName": "",  # Assuming default building name
                "events": [],
                "environment": [],
                "data": [],
                "plots": [{
                    "id": plot_id,
                    "plotName": "",  # Assuming default plot name
                    "data": [{
                        "date": plot_date,
                        "area": 0,
                        "fruitlets": 0,
                        "height": 0,
                        "leaves": 0,
                        "volume": 0,
                        "width": new_plot_width
                    }]
                }]
            }
            farm["buildings"].append(new_building)
            return data  # Return the updated data structure
    # If farm ID not found, add a new farm with the building, plot, and data
    new_farm = {
        "id": farm_id,
        "farmName": "",  # Assuming default farm name
        "buildings": [{
            "id": building_id,
            "buildingName": "",  # Assuming default building name
            "events": [],
            "environment": [],
            "data": [],
            "plots": [{
                "id": plot_id,
                "plotName": "",  # Assuming default plot name
                "data": [{
                    "date": plot_date,
                    "area": 0,
                    "fruitlets": 0,
                    "height": 0,
                    "leaves": 0,
                    "volume": 0,
                    "width": new_plot_width
                }]
            }]
        }]
    }
    data.append(new_farm)
    return data  # Return the updated data structure
