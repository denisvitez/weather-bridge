import os


def parse_string_to_key_pair(content: str, character: str = "&"):
    data = dict()
    pairs = content.split(character)
    for p in pairs:
        key, value = p.split("=")
        if key not in data.keys():
            data[key] = value
    return data


def fahrenheit_to_celsius(val_f: float):
    return (val_f - 32) * (5/9)


def miles_to_kph(val_mph: float):
    return val_mph * 1.60934


def inches_to_mm(val_in: float):
    return val_in * 25.4


def converter(data: dict, key: str, new_key: str, converter_func):
    if key in data.keys():
        data[new_key] = converter_func(float(data[key]))


def convert_units_temp(data: dict):
    converter(data, "tempf", "temp", fahrenheit_to_celsius)
    converter(data, "tempinf", "tempin", fahrenheit_to_celsius)


def convert_units_speed(data: dict):
    converter(data, "windspeedmph", "windspeedkph", miles_to_kph)
    converter(data, "windgustmph", "windgustkph", miles_to_kph)
    converter(data, "maxdailygust", "maxdailygustkph", miles_to_kph)


def convert_units_depth(data: dict):
    converter(data, "rainratein", "rainratemm", inches_to_mm)
    converter(data, "eventrainin", "eventrainmm", inches_to_mm)
    converter(data, "hourlyrainin", "hourlyrainmm", inches_to_mm)
    converter(data, "dailyrainin", "dailyrainmm", inches_to_mm)
    converter(data, "weeklyrainin", "weeklyrainmm", inches_to_mm)
    converter(data, "monthlyrainin", "monthlyrainmm", inches_to_mm)
    converter(data, "totalrainin", "totalrainmm", inches_to_mm)


def add_env_to_dict(data: dict, key: str, is_secret=False):
    val = os.getenv(key, None)
    if is_secret and val:
        val = "****"
    data[key] = val


def get_data_dict(data: dict):
    relevant_data = dict()
    if os.getenv("CONVERT_TEMP", False):
        relevant_data["temp"] = data["temp"]
        relevant_data["tempin"] = data["tempin"]
    else:
        relevant_data["tempf"] = data["tempf"]
        relevant_data["tempinf"] = data["tempinf"]
    if os.getenv("CONVERT_SPEED", False):
        relevant_data["windspeedkph"] = data["windspeedkph"]
        relevant_data["windgustkph"] = data["windgustkph"]
        relevant_data["maxdailygustkph"] = data["maxdailygustkph"]
    else:
        relevant_data["windspeedmph"] = data["windspeedmph"]
        relevant_data["windgustmph"] = data["windgustmph"]
        relevant_data["maxdailygust"] = data["maxdailygust"]
    if os.getenv("CONVERT_DEPTH", False):
        relevant_data["rainratemm"] = data["rainratemm"]
        relevant_data["eventrainmm"] = data["eventrainmm"]
        relevant_data["hourlyrainmm"] = data["hourlyrainmm"]
        relevant_data["dailyrainmm"] = data["dailyrainmm"]
        relevant_data["weeklyrainmm"] = data["weeklyrainmm"]
        relevant_data["monthlyrainmm"] = data["monthlyrainmm"]
        relevant_data["totalrainmm"] = data["totalrainmm"]
    else:
        relevant_data["rainratein"] = data["rainratein"]
        relevant_data["eventrainin"] = data["eventrainin"]
        relevant_data["hourlyrainin"] = data["hourlyrainin"]
        relevant_data["dailyrainin"] = data["dailyrainin"]
        relevant_data["weeklyrainin"] = data["weeklyrainin"]
        relevant_data["monthlyrainin"] = data["monthlyrainin"]
        relevant_data["totalrainin"] = data["totalrainin"]
    relevant_data['solarradiation'] = data["solarradiation"]
    relevant_data['uv'] = data["uv"]
    return relevant_data


def send_mqtt(mqtt_client, topic: str, data: dict):
    for key in data.keys():
        msg_topic = topic + "/" + key
        print("Sending MQTT to: ", msg_topic)
        mqtt_client.publish(msg_topic, data[key])
