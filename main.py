from website import crear_aplicacion

app = crear_aplicacion()

if __name__ == '__main__':
    app.run(debug=True)