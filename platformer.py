from pgzero.builtins import Actor

def build(csv_file, tile_size):
    """
    Constrói uma lista de Atores a partir de um arquivo CSV.
    Cada bloco no arquivo CSV é representado por seu ID.
    A função cria um Ator para cada bloco com a imagem correspondente.
    """
    objects = []
    with open(csv_file, 'r') as f:
        for y, line in enumerate(f):
            row = line.strip().split(',')
            for x, tile_id in enumerate(row):
                if tile_id != '-1':
                    image_name = f'tile_{int(tile_id):04d}'
                    actor = Actor(image_name)
                    actor.topleft = (x * tile_size, y * tile_size)
                    objects.append(actor)
    return objects
