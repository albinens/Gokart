# from flask-server.Model import Model
from model.Model import Model


class Main():

    def __init__(self) -> None:
        self.__model = Model()

    def main(self):
        self.__model.run()


# if __name__ == "__main__":
#    main = Main()
#    main.main()
