

def filter_females(indicators, groups=None):

    valid_groups = ["G1","G2","G3"]

    if groups:
        for group in groups:
            if group not in valid_groups:
                msg = f"{group} is not a valid group. Must be in 'G1','G2','G3'."
                raise ValueError(msg)
                
    groups = groups or valid_groups

    females = []

    groups = groups or valid_groups
    
    for l in indicators:
        match = None
        if ("G1" in groups) and (l[0] == l[3]):
            match = l
        if ("G2" in groups) and (l[1] == l[4]):
            match = l
        if ("G3" in groups) and (l[2] == l[5]):
            match = l
        if match:
            females.append(match)

    unique_females = list(set(females))

    return unique_females
