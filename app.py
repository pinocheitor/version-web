from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Función para formatear el ticket
def format_ticket(title, prefijo='RPA --', subticket_prefix='OLT BACKHAUL ---'):
    try:
        # Verificar si el título contiene la estructura esperada
        if 'ALARMA ACTIVA:' not in title or 'Puertas' not in title:
            raise ValueError("El formato del título de alarma no es válido")

        # Extracción de datos relevantes del título original
        parts = title.split(':')
        if len(parts) < 3:
            raise ValueError("El formato del título de alarma no es válido")

        olt_info = parts[1].strip().replace('OLT-', '')  # Corregir la duplicación de 'OLT-'
        puertas_info = parts[2].split('- Puertas', 1)[0].strip()
        onts_info = ""

        if 'ONTs Afectadas:' in title:
            start_index = title.index("[ONTs Afectadas:") + len("[ONTs Afectadas:")
            end_index = title.index("]", start_index)
            onts_info = " -- DOWN [ONTs Afectadas: " + title[start_index:end_index] + "]"

        # Construcción del nuevo título con ONTs afectadas
        formatted_title = f"{prefijo} OLT-{olt_info} - Puertas -- {puertas_info}{onts_info}"

        # Construcción del subticket
        subticket = f"{subticket_prefix} {formatted_title}"

        return formatted_title, subticket

    except (IndexError, ValueError) as e:
        return f"Error: {str(e)}", "Error"

# Ruta para la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    formatted_title = ""
    subticket = ""

    if request.method == 'POST':
        new_alarm = request.form['title']
        formatted_title, subticket = format_ticket(new_alarm)
        if isinstance(formatted_title, str) and isinstance(subticket, str):
            flash('Ticket generado correctamente', 'success')
        else:
            flash('Error al generar el ticket', 'error')

    return render_template('index.html', title="", ticket=formatted_title, subticket=subticket)

if __name__ == '__main__':
    app.run(debug=True)
