from flask import request, session 

def process_data(converter, conv_id):
    results={}
    input_vals={}
    data = request.form.getlist("value")
    data = [float(d) for d in data]

    form_type = converter["type"] if converter else None

    if form_type=="single":
        print('entra single')
        value=data[0]
        unit = request.form["unit"]
        print(unit)
        unit_res, unit_in = unit.split("_")

        if converter:
            print('entra converter')
            result_value = converter["formula"](data, unit_res)
            results["result"] = result_value
            results["conv_id"] = conv_id
            results["string"]=f"{value} ({unit_in}) → {result_value} ({unit_res})"

            input_vals["conv_id"] = conv_id
            input_vals["value"] = value

        else:
            results["string"] = "⚠️ Conversor no encontrado."
    
    else:
        if converter:
            result_value = converter["formula"](data)
            unit_res = converter["unit_res"]
            results["result"] = result_value
            results["conv_id"] = conv_id
            results["string"] = f"Resultado: {result_value} ({unit_res})"
    
    session["results"] = results
    session["input_vals"] = input_vals