from my_app import app

app.config.from_object('config.DevelopmentConfig')

app.run()