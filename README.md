# Time for Vbus API

Time for Vbus API wraps the WSDL service of Vitrasa for get the stops and the
buses estimates in JSON format.


## Endpoints

* [Get all stops][#get-all-stops]
* [Get stops around][#get-stops-around]
* [Get stop][#get-stop]

### Get all stops

``` http
GET /stops
```

Example:

``` http
GET /stops

{
    "stops": [
        {
            "number": 20,
            "name": "Abade Juan de Bastos, (C.C.Freixo)",
            "location": {
                "lng": -8.74098135187851,
                "lat": 42.1874372819504
            }
        },
        {
            "number": 40,
            "name": "Abade Juan de Bastos, 48",
            "location": {
                "lng": -8.73182995565854,
                "lat": 42.1913070501787
            }
        }
    ]
}
```


### Get stops around

``` http
GET /stops?lat=<latitude>&lng=<longitude>
```

Example:

``` http
GET /stops?lat=42.2260892&lng=-8.7254259

{
    "stops": [
        {
            "number": 14255,
            "name": "Pintor Colmeiro 23",
            "location": {
                "lng": -8.72577877618138,
                "lat": 42.2253189833775
            },
            "distance": 136.092
        },
        {
            "number": 2450,
            "name": "Barcelona,36",
            "location": {
                "lng": -8.72371600770132,
                "lat": 42.2259534895588
            },
            "distance": 212.8333
        }
    ]
}
```


### Get stop

``` http
GET /stops/<stop_number>
```

Example:

``` http
GET /stops/14255

{
    "number": 14255,
    "name": "Pintor Colmeiro 23",
    "location": {
        "lng": -8.72577877618138,
        "lat": 42.2253189833775
    }
}
```

