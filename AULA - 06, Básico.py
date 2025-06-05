# Criando um dicionário
aluno = {
"nome": "Erick",
"idade": 18,
"curso": "Engenharia da Computação"
}
# Visualizando o os dados
print("Nome:", aluno["nome"])
print("Idade:", aluno["idade"])
print("Curso:", aluno["curso"])

# Adicionando um novo campo
aluno["matricula"] = "153088"
# Atualizando um valor
aluno["idade"] = 21
# Exibindo todos os dados atualizados
print("\nDados atualizados do aluno:"),
for chave, valor in aluno.items():
    print(f"{chave}: {valor}")
