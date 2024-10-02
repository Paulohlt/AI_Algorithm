from kanren import Relation, facts, var, run, lall
from kanren.constraints import neq

# Definindo a relação de parentesco
parente = Relation()

# Lista com a árvore genealógica com todas gerações 
geracao1 = ("Eric","Carol","Thomas","Olga","Ken","Renata")
geracao2 = ("John","Julia","Leo","Angela","Karen","Rodrigo")
geracao3 = ("Lisa","Bia","Arthur","Cris","Silvia")

# Predicados: Fatos das relações de parentesco
facts(parente, 
      (geracao1[1], geracao2[0]),  # Carol é mãe de John
      (geracao1[1], geracao2[1]),  # Carol é mãe de Julia
      (geracao1[1], geracao1[2]),  # Carol é mãe de Leo
      (geracao1[3], geracao2[3]),  # Olga é mãe de Angela
      (geracao1[3], geracao2[4]),  # Olga é mãe de Karen 
      (geracao1[5], geracao2[5]),  # Renata é mãe de Rodrigo
      (geracao2[3], geracao3[0]),  # Angela é mãe de Lisa
      (geracao2[3], geracao3[1]),  # Angela é mãe de Bia
      (geracao2[3], geracao3[2]),  # Angela é mãe de Arthur
      (geracao2[4], geracao3[3]),  # Karen é mãe de Cris
      (geracao2[4], geracao3[4]),  # Karen é mãe de Silvia
      (geracao1[0], geracao2[0]),  # Eric é pai de John
      (geracao1[0], geracao2[1]),  # Eric é pai de Julia
      (geracao1[0], geracao2[2]),  # Eric é pai de Leo  
      (geracao1[2], geracao2[3]),  # Thomas é pai de Angela
      (geracao1[2], geracao2[4]),  # Thomas é pai de Karen
      (geracao1[4], geracao2[5]),  # Ken é pai de Rodrigo
      (geracao2[2], geracao3[0]),  # Leo é pai de Lisa   
      (geracao2[2], geracao3[1]),  # Leo é pai de Bia  
      (geracao2[2], geracao3[2]),  # Leo é pai de Arthur
      (geracao2[5], geracao3[3]),  # Rodrigo é pai de Cris
      (geracao2[5], geracao3[4])   # Rodrigo é pai de Silvia
)


# Definindo variáveis lógicas para consultas
filho = var()
pai_mae = var()
avo = var() 
irmao = var()

# Função para encontrar os pais de uma pessoa
def encontrar_pais(pessoa):
    """
    Retorna os pais de uma pessoa: str
    """
    return run(0, pai_mae, parente(pai_mae, pessoa))

# Função para encontrar os filhos de uma pessoa
def encontrar_filhos(pessoa):
    """
    Retorna os filhos de uma pessoa: str
    """
    return run(0, filho, parente(pessoa, filho))

# Função para encontrar os irmãos de uma pessoa
def encontrar_irmaos(pessoa):
    """
    Retorna os irmãos de uma pessoa: str
    """
    return tuple(set(run(0, irmao, lall(  # A funçao set evita valores duplicados e permite irmãos de pais diferentes
        parente(pai_mae, irmao),          # irmao é filho de pai_mae
        parente(pai_mae, pessoa),         # pessoa é filho de pai_mae
        neq(irmao, pessoa)                # O irmão não pode ser a própria pessoa
    ))))

# Função para encontrar os avós de uma pessoa
def encontrar_avos(pessoa):
    """
    Retorna os avós de uma pessoa: str
    """
    return run(0, avo, lall(
        parente(avo, pai_mae),   # avo é filho de pai/mãe 
        parente(pai_mae, pessoa) # pessoa é filha de pai_mae
    ))

# Função para encontrar os netos de uma pessoa
def encontrar_netos(pessoa):
    """
    Retorna os netos de uma pessoa: str
    """
    return run(0, filho, lall(    
        parente(pessoa, pai_mae), # pessoa é pai de pai_mae
        parente(pai_mae, filho)   # pai_mae é pai de filho, ou seja, neto de pessoa
    ))

# Função para encontrar tios de uma pessoa
def encontrar_tios(pessoa):
    """
    Retorna os tios de uma pessoa: str
    """
    return tuple(set(run(0, irmao, lall( # A funçao set evita valores duplicados e permite tios de pais diferentes
        parente(pai_mae, pessoa),  # pai/mãe é filho da pessoa
        parente(avo, irmao),       # irmao é filho de avo
        parente(avo, pai_mae),     # pai/mãe é filho de avo
        neq(irmao, pai_mae)        # O tio não pode ser o próprio pai/mãe
    ))))

# Solução
for nome in geracao3:
    print(f"Pais de {nome}:", encontrar_pais(f"{nome}"))
    print(f"Irmãos de {nome}:", encontrar_irmaos(f"{nome}"))
    print(f"Tios de {nome}:", encontrar_tios(f"{nome}"))
    print(f"Avós de {nome}:", encontrar_avos(f'{nome}'))

for nome in geracao2:
    print(f"Pais de {nome}:", encontrar_pais(f"{nome}"))
    print(f"Irmãos de {nome}:", encontrar_irmaos(f"{nome}"))
    print(f"Filhos de {nome}:", encontrar_filhos(f"{nome}"))

for nome in geracao1:
    print(f"Filhos de {nome}:", encontrar_filhos(f"{nome}"))
    print(f"Netos de {nome}:", encontrar_netos(f"{nome}"))

