import math
from flask import Flask, render_template, request

app = Flask(__name__)

def isentropic_flow_relations(M, gamma):
    temp_ratio = 1 / (1 + (gamma - 1) / 2 * M ** 2)
    pressure_ratio = temp_ratio ** (gamma / (gamma - 1))
    density_ratio = temp_ratio ** (1 / (gamma - 1))
    area_ratio = (1 / M) * ((2 / (gamma + 1)) * (1 + (gamma - 1) / 2 * M ** 2)) ** ((gamma + 1) / (2 * (gamma - 1)))
    return {
        "Temperature Ratio (T/T0)": temp_ratio,
        "Pressure Ratio (p/p0)": pressure_ratio,
        "Density Ratio (rho/rho0)": density_ratio,
        "Area Ratio (A/A*)": area_ratio
    }

def normal_shock_relations(M1, gamma):
    M2 = math.sqrt((1 + (gamma - 1) / 2 * M1 ** 2) / (gamma * M1 ** 2 - (gamma - 1) / 2))
    temp_ratio = ((1 + (gamma - 1) / 2 * M1 ** 2) * (2 * gamma * M1 ** 2 - (gamma - 1))) / ((gamma + 1) ** 2 * M1 ** 2)
    pressure_ratio = 1 + 2 * gamma / (gamma + 1) * (M1 ** 2 - 1)
    density_ratio = ((gamma + 1) * M1 ** 2) / ((gamma - 1) * M1 ** 2 + 2)
    stagnation_pressure_ratio = pressure_ratio / (density_ratio ** gamma)
    return {
        "Downstream Mach Number (M2)": M2,
        "Temperature Ratio (T2/T1)": temp_ratio,
        "Pressure Ratio (p2/p1)": pressure_ratio,
        "Density Ratio (rho2/rho1)": density_ratio,
        "Stagnation Pressure Ratio (p02/p01)": stagnation_pressure_ratio
    }

def oblique_shock_relations(M1, beta, gamma):
    beta_rad = math.radians(beta)
    M1n = M1 * math.sin(beta_rad)
    denominator = gamma * M1n ** 2 - (gamma - 1) / 2
    if denominator <= 0:
        return {"error": "Invalid input leading to math domain error."}
    M2 = math.sqrt((1 + (gamma - 1) / 2 * M1n ** 2) / denominator)
    temp_ratio = ((1 + (gamma - 1) / 2 * M1n ** 2) * (2 * gamma * M1n ** 2 - (gamma - 1))) / ((gamma + 1) ** 2 * M1n ** 2)
    pressure_ratio = 1 + 2 * gamma / (gamma + 1) * (M1n ** 2 - 1)
    density_ratio = ((gamma + 1) * M1n ** 2) / ((gamma - 1) * M1n ** 2 + 2)
    delta_rad = math.atan((2 / math.tan(beta_rad)) * (M1 ** 2 * math.sin(beta_rad) ** 2 - 1) /
                          (M1 ** 2 * (gamma + math.cos(2 * beta_rad)) + 2))
    delta_deg = math.degrees(delta_rad)
    return {
        "Downstream Mach Number (M2)": M2,
        "Temperature Ratio (T2/T1)": temp_ratio,
        "Pressure Ratio (p2/p1)": pressure_ratio,
        "Density Ratio (rho2/rho1)": density_ratio,
        "Deflection Angle (delta)": delta_deg
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/isentropic', methods=['GET', 'POST'])
def isentropic():
    if request.method == 'POST':
        try:
            M = float(request.form['mach'])
            gamma = float(request.form['gamma'])
            results = isentropic_flow_relations(M, gamma)
            return render_template('isentropic.html', results=results)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('isentropic.html')

@app.route('/normal_shock', methods=['GET', 'POST'])
def normal_shock():
    if request.method == 'POST':
        try:
            M = float(request.form['mach'])
            gamma = float(request.form['gamma'])
            results = normal_shock_relations(M, gamma)
            return render_template('normal_shock.html', results=results)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('normal_shock.html')

@app.route('/oblique_shock', methods=['GET', 'POST'])
def oblique_shock():
    if request.method == 'POST':
        try:
            M = float(request.form['mach'])
            beta = float(request.form['beta'])
            gamma = float(request.form['gamma'])
            results = oblique_shock_relations(M, beta, gamma)
            return render_template('oblique_shock.html', results=results)
        except Exception as e:
            return f"An error occurred: {str(e)}"
    return render_template('oblique_shock.html')