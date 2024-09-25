from kanren import Relation, facts, var, run, lall, lany
from kanren.constraints import neq

# Atribui os predicados
mae = Relation()
pai = Relation()

# Relações de mães
facts(mae, 
      ('Carol', 'John'),
      ('Carol', 'Julia'),
      ('Carol', 'Leo'),
      ('Olga', 'Angela'),
      ('Olga', 'Karen'),
      ('Renata', 'Rodrigo'),
      ('Angela', 'Lisa'),
      ('Angela', 'Bia'),
      ('Angela', 'Arthur'),
      ('Karen', 'Cris'),
      ('Karen', 'Silvia')
)

# Relações de pais
facts(pai, 
      ('Eric', 'John'),
      ('Eric', 'Julia'),
      ('Eric', 'Leo'),
      ('Thomas', 'Angela'),
      ('Thomas', 'Karen'),
      ('Ken', 'Rodrigo'),
      ('Leo', 'Lisa'),
      ('Leo', 'Bia'),
      ('Leo', 'Arthur'),
      ('Rodrigo', 'Cris'),
      ('Rodrigo', 'Silvia')
)

# Função genérica para encontrar parentes (pais, avós, etc.)
def encontrar_parentes(tipo_relacao, pessoa, parente=None):
    if parente is None:
        parente = var()
    return run(0, parente, lany(
        tipo_relacao(mae, pessoa, parente),
        tipo_relacao(pai, pessoa, parente)
    ))

# Função para verificar relações (como pais, avós, etc.)
def relacao(relation, pessoa, parente=None):
    if parente is None:
        parente = var()
    return run(0, parente, relation(pessoa, parente))

# Função para encontrar avós (pode ser usado para avós paternos ou maternos)
def encontrar_avos(relacao_filho, pessoa):
    avo = var()
    pai_mae = var()
    return run(0, avo, lall(
        lany(mae(avo, pai_mae), pai(avo, pai_mae)),
        relacao_filho(pai_mae, pessoa)
    ))

# Função que encontra os avós (maternos e paternos)
def avos(pessoa):
    return encontrar_avos(pai, pessoa) + encontrar_avos(mae, pessoa)

# Função para encontrar irmãos de uma pessoa
def irmaos(pessoa):
    irmao = var()
    mae_pai = var()
    return set(run(0, irmao, lall(
        lany(mae(mae_pai, irmao), pai(mae_pai, irmao)),
        lany(mae(mae_pai, pessoa), pai(mae_pai, pessoa)),
        neq(irmao, pessoa)
    )))

# Variáveis
x = var()

# Saída dos resultados
print("Pais de Lisa: ", encontrar_parentes(lambda rel, pessoa, parente: rel(parente, pessoa), "Lisa"))
print("Filhos: ", encontrar_parentes(lambda rel, pessoa, parente: rel(pessoa, parente), "Angela"))
print("Irmãos: ", irmaos('Leo'))
print("Avós Paternos: ", encontrar_avos(pai, 'Bia'))
print("Avós Maternos: ", encontrar_avos(mae, "Cris"))
print("Avós: ", avos("Arthur"))
