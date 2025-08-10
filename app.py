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

@app.route("/hidro")
def hidro():
    return render_template("index.html")

@app.route("/daso")
def daso():
    return render_template("index.html")

@app.route("/selvi")
def selvi():
    return render_template("index.html")