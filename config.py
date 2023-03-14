from importlib import resources
import json
import os


class Config:

    __instance = None
    constantes = None

    @staticmethod
    def instance():
        if Config.__instance is None:
            Config()
            print(id(Config.__instance))
        return Config.__instance 
        
    def __init__(self):
        if Config.__instance is None:
            Config.__instance  = self

            json_file = open("config.json")
            self.constantes = json.load(json_file)
            print(self.constantes["blanco"])
            json_file.close

        else:
            raise exception ("Config cannot have mutiple instances")

        pass

    