def general():
    converters = [
        {
            "id": "ha_m2",
            "title": "Hectáreas ↔ Metros cuadrados",
            "description": "Convierte fácilmente entre hectáreas y metros cuadrados.",
            "units": [
                {"unit_in": "ha", "unit_res": "m2", "label": "Hectáreas → Metros cuadrados"},
                {"unit_in": "m2", "unit_res": "ha", "label": "Metros cuadrados → Hectáreas"}
            ],
            "formula": lambda value, unit: value * 10000 if unit == "m2" else value / 10000
        }
    ]
    return converters