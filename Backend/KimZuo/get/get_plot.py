def get_plot_data(data, farm_id, building_id, plot_id):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            return plot
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotName(data, farm_id, building_id, plot_id):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            plotName = plot["plotName"]
                            return plotName
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotArea(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_area = existing_data["area"]
                                    return plot_area
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotFruitlets(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_fruitlets = existing_data["fruitlets"]
                                    return plot_fruitlets
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotHeight(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_height = existing_data["height"]
                                    return plot_height
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotLeaves(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_leaves = existing_data["leaves"]
                                    return plot_leaves
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotVolume(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_volume = existing_data["volume"]
                                    return plot_volume
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")


def get_plotWidth(data, farm_id, building_id, plot_id, plot_date):
    for farm in data:
        if farm["id"] == farm_id:
            for building in farm["buildings"]:
                if building["id"] == building_id:
                    for plot in building["plots"]:
                        if plot["id"] == plot_id:
                            for existing_data in plot["data"]:
                                if existing_data["date"] == plot_date:
                                    # Update existing plot data
                                    plot_width = existing_data["width"]
                                    return plot_width  # Return the updated data structure
                            # If plot data for the date not found, return error
                            raise ValueError("Plot date not found")
                    # If plot id not found, return error
                    raise ValueError("Plot ID not found")
            # If build ID not found, return error
            raise ValueError("Building ID not found")
    # If farm ID not found, return error
    raise ValueError("Farm ID not found")
