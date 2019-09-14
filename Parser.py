import regex as re

rx_dict = {
    'name': re.compile(r'NAME : (?P<name>.*)'),
    'comment': re.compile(r'COMMENT : [(]Augerat et al, Min no of trucks: (?P<minNumVehicles>[0-9]*), (Optimal|Best) value: (?P<optimalValue>[0-9]*)[)]\n'),
    'capacity': re.compile(r'CAPACITY : (?P<capacity>[0-9]+)\n'),
    'node_coord': re.compile(r'NODE_COORD_SECTION'),
    'demand_values': re.compile(r'DEMAND_SECTION'),
    'values' : re.compile(r'[0-9]* (?P<x>[0-9]+) (?P<y>[0-9]+)?') # test this
}

def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None
def parse_file(filepath):
    """
    Parse text at given filepath

    Parameters
    ----------
    filepath : str
        Filepath for file_object to be parsed

    Returns
    -------
    listCoords : [x,y] - contains list of coordinates of each node
    listDemand : x - contains list of demand of each node
    InstanceData : ['Name', 'MinNumVehicles', 'OptimalValue', 'Capacity']
    """

    InstanceData = []

    listCoords = []  # create an empty list to collect node coordinates
    listDemand = []  # create an empty list to collect node demand

    IsNodeCoord = False
    IsDemandValue = False
    # open the file and read through it line by line
    with open(filepath, 'r') as file_object:
        line = file_object.readline()
        while line:
            # at each line check for a match with a regex
            key, match = _parse_line(line)

            if key == 'name':
                name = match.group('name')
            elif key == 'comment':
                minNumVehicles = int(match.group('minNumVehicles'))
                optimalValue = int(match.group('optimalValue'))
            elif key == 'capacity':
                capacity = int(match.group('capacity'))
                InstanceData = {
                    'Name': name,
                    'MinNumVehicles': minNumVehicles,
                    'OptimalValue' : optimalValue,
                    'Capacity' : capacity
                }
                
            elif key == 'node_coord':
                IsNodeCoord = True
            elif key == 'demand_values':
                IsNodeCoord = False
                IsDemandValue = True
            elif IsNodeCoord and key == 'values':
                x = int(match.group('x'))
                y = int(match.group('y'))
                coord = [x,y]
                listCoords.append(coord)
            elif IsDemandValue and key == 'values':
                demand = int(match.group('x'))
                listDemand.append(demand)
            line = file_object.readline()

    return listCoords, listDemand, InstanceData
