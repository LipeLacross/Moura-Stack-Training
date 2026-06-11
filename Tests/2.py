import time

def gerador_notas_fiscais(quantidade):
    for i in range (quantidade):
        time.sleep(1)
        yield f'nota fiscal {i+1}'

print(f"iniciando simulação")

notas_fiscais = gerador_notas_fiscais(5)
for nota in notas_fiscais:
    print(nota)
    time.sleep(3)


print(f"lote processado")