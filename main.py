from website import create_app

app = create_app()

if __name__ == '__main__':
    # anytime we change smth in code, debug True reruns server, so changes applies
    app.run(debug=True)
