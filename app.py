from sqlite3 import converters
from flask import Flask, render_template, request, redirect, url_for, session
from . import conv_list, utils

app = Flask(__name__)
app.secret_key="jv<?8._BOM'QDqciW1Dx"

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/", methods=['POST', 'GET'])
def main():
    converters=conv_list.general()
    results={}
    input_vals={}

    if request.method == "POST":
        try:
            conv_id = request.form["converter_id"]

            converter = next((c for c in converters if c["id"] == conv_id), None)
            utils.process_data(converter, conv_id)
            
            return redirect(url_for("main") + f"#{conv_id}")
        except ValueError as e:
            print("ERROR")
            print(e)
    else:
        results=session.pop("results", {})
        input_vals=session.pop("input_vals", {})
        
    return render_template("index.html", converters=converters, results=results, input_vals=input_vals)

@app.route("/cubic", methods=["POST", "GET"])
def cubic():
    province_list = utils.get_provinces()
    if request.method == "POST":
        try:
            id=request.form["id"]

            province=request.form["province"]
            species_list=utils.get_values(province, "ESPECIE")
            cubic_list=utils.get_values(province, "FORMA DE CUBICACIÓN")
            out_list=utils.get_values(province, "PARÁMETRO")

            session["species_list"] = species_list
            session["cubic_list"] = cubic_list
            session["out_list"] = out_list

            if id=="select_province":
                session["selection"] = {
                    "province": province,
                    "species": "",
                    "cubication": "",
                    "out": "",
                    "Dn": "",
                    "Ht": ""
                }

                return redirect(url_for("cubic"))

            else:
                province = request.form["province"]
                output = request.form["outs"]
                species = request.form["species"]
                cubication = int(request.form["cubication"])
                Dn = float(request.form["Dn"])
                Ht = float(request.form["Ht"])


                print(province, output, species, cubication)

                session['result']=utils.cubication(output, province, species, cubication, Dn, Ht)
                session["selection"] = {
                    "province": province,
                    "species": species,
                    "cubication": cubication,
                    "Dn": Dn,
                    "Ht": Ht,
                    "out": output
                }

                return redirect(url_for("cubic"))
            
        except ValueError as e:
            print("ERROR")
            print(e)
    else:
        species_list = session.pop("species_list", [])
        cubic_list = session.pop("cubic_list", [])
        out_list = session.pop("out_list", [])
        result = session.pop("result", None)
        selection = session.pop("selection", {})
        print(selection)

        if result is None:
            result={
            'value': None,
            'units': ''
        }
        elif result=='fail':
            result={
            'value': 'Parámetros no válidos',
            'units': ''
        }
        else:
            result={
            'value': result,
            'units': 'dm3'
        }

        return render_template("cubic.html", result=result, species_list=species_list, cubic_list=cubic_list,
                               province_list=province_list, out_list=out_list, selection=selection)

