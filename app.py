from flask import Flask, render_template, request
from . import conv_list

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/", methods=['POST', 'GET'])
def main():
    converters=conv_list.general()
    results={}
    input_val=0

    if request.method == "POST":
        try:
            value = float(request.form["value"])
            
            unit = request.form["unit"]

            unit_res, unit_in = unit.split("_")

            conv_id = request.form["converter_id"]

            converter = next((c for c in converters if c["id"] == conv_id), None)
            if converter:
                result_value = converter["formula"](value, unit_res)
                results[conv_id] = f"{value} ({unit_in}) → {result_value} ({unit_res})"
                input_val = value
            else:
                results[conv_id] = "⚠️ Conversor no encontrado."
        except ValueError:
            results[request.form["converter_id"]] = "⚠️ Introduce un número válido."

    return render_template("index.html", converters=converters, results=results, input_val=input_val)

@app.route("/hidro")
def hidro():
    return render_template("index.html")

@app.route("/daso")
def daso():
    return render_template("index.html")

@app.route("/selvi")
def selvi():
    return render_template("index.html")