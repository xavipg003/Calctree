def general():
    converters = [
        {
            "id": "ha_m2",
            "title": "Hectáreas ↔ Metros cuadrados",
            "description": "Convierte fácilmente entre hectáreas y metros cuadrados.",
            "type": "single",
            "units": [
                {"unit_in": "ha", "unit_res": "m2", "label": "Hectáreas → Metros cuadrados"},
                {"unit_in": "m2", "unit_res": "ha", "label": "Metros cuadrados → Hectáreas"}
            ],
            "formula": lambda data, unit: data[0] * 10000 if unit == "m2" else data[0] / 10000
        },
        {
            "id": "vol_madera",
            "title": "Volumen de madera (aproximado)",
            "description": "Calcula el volumen en m³ de un árbol dado su diámetro (m) y altura (m), asumiendo forma cilíndrica.",
            "type": "multi",
            "units_in": ["Diámetro (m)", "Altura (m)"],
            "unit_res": "m³",
            "formula": lambda data: 3.1416 * ((data[0]/2) ** 2) * data[1]  
        },
        {
            "id": "temperatura",
            "title": "Temperatura °C ↔ °F",
            "description": "Convierte entre grados Celsius y Fahrenheit.",
            "type": "single",
            "units": [
                {"unit_in": "C", "unit_res": "F", "label": "Celsius → Fahrenheit"},
                {"unit_in": "F", "unit_res": "C", "label": "Fahrenheit → Celsius"}
            ],
            "formula": lambda data, unit: (data[0] * 9/5) + 32 if unit == "F" else (data[0] - 32) * 5/9
        },
        {
            "id": "densidad_madera",
            "title": "Densidad de la madera",
            "description": "Calcula la densidad (kg/m³) a partir de la masa (kg) y volumen (m³).",
            "type": "multi",
            "units_in": ["Masa (kg)", "Volumen (m³)"],
            "unit_res": "kg/m³",
            "formula": lambda data: data[0] / data[1] if data[1] != 0 else None
        },
        {
            "id": "area_basal",
            "title": "Área basal de un árbol",
            "description": "Calcula el área basal en m² a partir del diámetro a la altura del pecho (DAP) en cm.",
            "type": "single",
            "units": [
                {"unit_in": "cm", "unit_res": "m²", "label": "DAP → Área basal"}
            ],
            "formula": lambda data, unit: 3.1416 * ((data[0]/200) ** 2)
        },
        {
            "id": "biomasa_arbol",
            "title": "Biomasa aérea (estimada)",
            "description": "Calcula la biomasa aérea (kg) usando un modelo alométrico simple: Biomasa = 0.05 × DAP² × Altura.",
            "type": "multi",
            "units_in": ["DAP (cm)", "Altura (m)"],
            "unit_res": "kg",
            "formula": lambda data: 0.05 * (data[0] ** 2) * data[1]
        },
        {
            "id": "carbono_forestal",
            "title": "Carbono almacenado",
            "description": "Calcula el carbono almacenado (toneladas) a partir de biomasa (ton) usando factor 0.5.",
            "type": "single",
            "units": [
                {"unit_in": "tonbiomasa", "unit_res": "tonC", "label": "Biomasa (ton) → Carbono (ton)"}
            ],
            "formula": lambda data, unit: data[0] * 0.5
        },
        {
            "id": "crecimiento_volumen",
            "title": "Incremento medio anual (IMA)",
            "description": "Calcula el incremento medio anual (m³/año) a partir de volumen final y edad.",
            "type": "multi",
            "units_in": ["Volumen final (m³)", "Edad (años)"],
            "unit_res": "m³/año",
            "formula": lambda data: data[0] / data[1] if data[1] != 0 else None
        }
    ]


    return converters