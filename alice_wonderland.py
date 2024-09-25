from kanren import Relation, facts, var, run, lall, lany, conde

# Predicado ontem(x, y): x é o dia que vem depois de y
ontem = Relation()
facts(ontem, 
      ('terça', 'segunda'),
      ('quarta', 'terça'),
      ('quinta', 'quarta'),
      ('sexta', 'quinta'),
      ('sábado', 'sexta'),
      ('domingo', 'sábado'),
      ('segunda', 'domingo'))

# Predicado mentira(x, y): x mente no dia y
mentira = Relation()
facts(mentira,
      ('leão', 'segunda'),
      ('leão', 'terça'),
      ('leão', 'quarta'),
      ('unicórnio', 'quinta'),
      ('unicórnio', 'sexta'),
      ('unicórnio', 'sábado'))

# Predicado verdade(x, y): x diz a verdade no dia y
verdade = Relation()
facts(verdade,
      ('leão', 'quinta'),
      ('leão', 'sexta'),
      ('leão', 'sábado'),
      ('leão', 'domingo'),
      ('unicórnio', 'domingo'),
      ('unicórnio', 'segunda'),
      ('unicórnio', 'terça'),
      ('unicórnio', 'quarta'))

# Função genérica para lidar com unicórnio ou leão
def comportamento(animal, hoje):
    return lany(
        lall(
            lall(ontem(hoje, antes), verdade(animal, hoje)),
            lall(ontem(hoje, antes), mentira(animal, antes))
        ),
        lall(
            lall(ontem(hoje, antes), verdade(animal, antes)),
            lall(ontem(hoje, antes), mentira(animal, hoje))
        )
    )

# Função que verifica o dia em que unicórnio e leão têm o mesmo comportamento
def dia_verdade():
    return run(0, hoje, conde((comportamento('unicórnio', hoje), comportamento('leão', hoje))))

# Variáveis 
antes = var()
hoje = var()
animal = var()

# Saída dos resultados
print("Dias em que a sentença é verdadeira para o unicórnio: ", run(0, hoje, comportamento('unicórnio', hoje)))
print("Dias em que a sentença é verdadeira para o leão: ", run(0, hoje, comportamento('leão', hoje)))
print("Hoje é: ", dia_verdade())