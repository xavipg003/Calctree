from flask import request, session 
import pandas as pd

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

def cubication(output, province, species, cubication, Dn, Ht):
    df = pd.read_csv(f"tasas/{province}.csv")
    df["FORMA DE CUBICACIÓN"] = df["FORMA DE CUBICACIÓN"].astype(int)

    df_filtrado = df[(df["ESPECIE"] == species) & (df["PARÁMETRO"] == output) & (df["FORMA DE CUBICACIÓN"] == int(cubication))]
    df_filtrado = df_filtrado.replace("-", 0)
    if df_filtrado.empty:
        result='fail'
        return result
    A=float(df_filtrado["A"].values[0]) if float(df_filtrado["A"].values[0]) !=0 else None
    B=float(df_filtrado["B"].values[0]) if float(df_filtrado["B"].values[0]) !=0 else None
    C=float(df_filtrado["C"].values[0]) if float(df_filtrado["C"].values[0]) !=0 else None
    D=float(df_filtrado["D"].values[0]) if float(df_filtrado["D"].values[0]) !=0 else None
    P=float(df_filtrado["P"].values[0]) if float(df_filtrado["P"].values[0]) !=0 else None
    Q=float(df_filtrado["Q"].values[0]) if float(df_filtrado["Q"].values[0]) !=0 else None
    R=float(df_filtrado["R"].values[0]) if float(df_filtrado["R"].values[0]) !=0 else None
    DNM=None

    if "MODELO" in df_filtrado.columns:
        model=int(df_filtrado["MODELO"].values[0])
    else:
        model=int(df_filtrado["Modelo"].values[0])
    try:
        DNM=float(df_filtrado["DNM"].values[0]) if float(df_filtrado["DNM"].values[0]) !=0 else None
    except KeyError:
        pass

    if output=='VCC':
        result=get_vcc(A,B,Dn,Ht,P,Q,R)
    elif output=='VSC':
        vcc=get_vcc(A,B,Dn,Ht,P,Q,R)
        result=A+B*vcc+C*(vcc**2)

    elif output=='IAVC':
        if model==8:
            vcc=get_vcc(A,B,Dn,Ht,P,Q,R)
            result=A+B*vcc+C*(vcc**2)
        elif model==13:
            result=A+B*(Dn-DNM)
        elif model==14:
            result=P*(Dn**Q)
        elif model==16:
            result=A+B*(Dn**2)
        elif model==17:
            result=A+B*(Dn)+C*(Dn**2)
        elif model==19:
            result=A+B*(Dn)+C*(Dn**2)+D*(Dn**3)
        elif model==20:
            result=A+B*(Dn)+D*(Dn**3)
        elif model==21:
            result=C*(Dn**2)+D*(Dn**3)
        elif model==25:
            result=P*(Dn**Q)*(Ht**R)

    elif output=='VLE':
        if A is None:
            result=P*(Dn**Q)
        else:
            vcc=get_vcc(A,B,Dn,Ht,P,Q,R)
            result=A+B*vcc+C*(vcc**2)
    else:
        result='fail'
    
    return result

def get_vcc(A,B,Dn,Ht,P,Q,R):
    if A is not None and B is not None:
            vcc=A+B*(Dn**2)*Ht
    else:
        vcc=P*(Dn**Q)*(Ht**R)
    return vcc

def get_values(province, value):
    df = pd.read_csv(f"tasas/{province}.csv")
    df["FORMA DE CUBICACIÓN"] = df["FORMA DE CUBICACIÓN"].astype(int)

    valores = df[value].dropna().unique().tolist()

    return valores

def get_provinces():
    provinces=[
            'A_Coruña', 'Albacete', 'Alicante', 'Asturias', 'Ávila', 'Baleares',
            'Burgos', 'Canarias', 'Castellón', 'Cantabria', 'Cataluña',
            'Ciudad_real', 'Cuenca', 'Extremadura', 'Guadalajara',
            'Huesca', 'La_Rioja', 'León', 'Lugo', 'Madrid', 'Murcia', 'Navarra',
            'Ourense', 'Palencia', 'País_Vasco', 'Pontevedra', 'Salamanca',
            'Segovia', 'Soria', 'Teruel', 'Toledo', 'Valencia',
            'Valladolid', 'Zamora', 'Zaragoza'
        ]
    return provinces