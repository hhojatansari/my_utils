import json
from collections import namedtuple


data = '{"esm": "Hosein", "team_morede_alaghe": {"esm": "Esteghlal", "ghahremani": "** ~> Asia"}}'

# Parse JSON into an object with attributes corresponding to dict keys.
hosein = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))

print(hosein.esm)
print(hosein.team_morede_alaghe.esm)
print(hosein.team_morede_alaghe.ghahremani)
