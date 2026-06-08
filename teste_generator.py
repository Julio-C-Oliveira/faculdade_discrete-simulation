import simpy

class Pessoa:
    def __init__(
            self, env,
            nome,
            tempo_de_estudo,
            tempo_de_redes_sociais
            ):

        self.env = env 
        self.env.process(self.run())

        self.nome = nome
        self.tempo_de_estudo = tempo_de_estudo
        self.tempo_de_redes_sociais = tempo_de_redes_sociais

    def run(self):
        tempo_de_estudo = 2
        tempo_redes_sociais = 5
        while True:
            print(f"{self.nome} começou a estudar em {self.env.now}")

            yield self.env.timeout(self.tempo_de_estudo)

            print(f"{self.nome} foi para as redes sociais em {self.env.now}")
            yield self.env.timeout(self.tempo_de_redes_sociais)

env = simpy.Environment()
p1 = Pessoa(
        env = env,
        nome = "Luiz",
        tempo_de_estudo = 1,
        tempo_de_redes_sociais = 5
    )
p2 = Pessoa(
        env = env,
        nome = "Júlio",
        tempo_de_estudo = 7,
        tempo_de_redes_sociais = 1
    )
env.run(until=50)
