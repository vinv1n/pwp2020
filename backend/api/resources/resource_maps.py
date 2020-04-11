"""
This maps resources to database models in a way that collections are easy to construct

HOWTO:

foobar = {
    'attribute1': {
        'prompt': 'prompt of attribute 1, please refer to the apiary for these'
    }
}

"""

observation = {
    "temperature": {
        "prompt": "Temperature (degrees of Celsius)"
    },
    "wind": {
        "prompt": "Speed of wind (m/s)"
    },
    "wind-direction": {
        "prompt": "Direction of wind"
    },
    "humidity": {
        "prompt": "Humidity as a percentage"
    }
}