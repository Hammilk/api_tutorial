import pokebase as pb

chesto = pb.APIResource("berry", "chesto")
print(chesto.name)
charmander = pb.pokemon("charmander")
print(charmander.height)
