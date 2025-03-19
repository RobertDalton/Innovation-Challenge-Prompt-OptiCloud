# function_app.py
import azure.functions as func
import src.main


app = func.AsgiFunctionApp(app=src.main.app,http_auth_level=func.AuthLevel.ANONYMOUS)
