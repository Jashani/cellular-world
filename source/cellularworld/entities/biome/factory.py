from cellularworld.entities.biome import biome_type, city, forest, ice, sea, land


def new(biome, cell):
    biomes = {biome_type.BiomeType.ICE: ice.Ice(cell),
              biome_type.BiomeType.SEA: sea.Sea(cell),
              biome_type.BiomeType.CITY: city.City(cell),
              biome_type.BiomeType.FOREST: forest.Forest(cell),
              biome_type.BiomeType.LAND: land.Land(cell)}
    return biomes[biome]
