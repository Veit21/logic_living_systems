# self replicating program
class Replicator:

    def __init__(self):

        # tape
        self.phi = "# self replicating program\nclass Replicator:\n\n\tdef __init__(self):\n\n\t\t# tape" \
                   "\n\t\tself.phi = \"{0}\"\n\n\t\t# construction unit\n\t\tdef __a(self):\n\t\t\tprint(self.phi)" \
                   "\n\n\t\t# copy unit\n\t\tdef __b(self):\n\t\t\tself.phi = self.phi.format(self.phi)" \
                   "\n\n\t\t# control instance\n\t\tdef c(self):\n\t\t\tself.__b()\n\t\t\tself.__a()" \
                   "\n\n\nreplicator = Replicator()\nreplicator.c()"

    # construction unit
    def __a(self):
        print(self.phi)

    # copy unit
    def __b(self):
        self.phi = self.phi.format(self.phi)

    # control instance
    def c(self):
        self.__b()
        self.__a()


replicator = Replicator()
replicator.c()
