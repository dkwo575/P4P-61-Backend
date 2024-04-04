def update_or_add_plot_data(data, farm_id, building_id, plot_date, new_plot_data):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["date"] == plot_date:
                            # Update existing plot data
                            plot.update(new_plot_data)
                            return True
                    # If plot date not found, add a new plot with the provided data
                    new_plot = {"date": plot_date}
                    new_plot.update(new_plot_data)
                    building["plots"].append(new_plot)
                    return True
            # If building ID not found, add a new building with the plot
            new_plot = {"date": plot_date}
            new_plot.update(new_plot_data)
            building_data = {"id": building_id, "buildingName": "", "events": [], "environment": [],
                             "data": [], "plots": [new_plot]}
            farm["buildings"].append(building_data)
            return True
    # If farm ID not found, add a new farm with the building and plot
    new_plot = {"date": plot_date}
    new_plot.update(new_plot_data)
    data.append({
        "id": farm_id,
        "farmName": "",  # Empty farm name since it's not specified
        "buildings": [
            {
                "id": building_id,
                "buildingName": "",  # Empty building name since it's not specified
                "events": [],
                "environment": [],
                "data": [],
                "plots": [new_plot]
            }
        ]
    })
    return True


def update_or_add_plotName(data, farm_id, building_id, plot_id, new_plotName):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            plot["plotName"] = new_plotName
                            return True
                    # If plot ID not found, add a new plot with the provided data
                    building["plots"].append({
                        "id": plot_id,
                        "plotName": new_plotName
                    })
                    return True
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
            return True
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
    return True

