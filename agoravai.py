import pandas as pd
import random
import os
import numpy as np
import re

directory1 = '/home/rodrigo/Área de Trabalho/PT2_CARBU/VENDAS_INTECH'
files1 = os.listdir(directory1)

directory2 = '/home/rodrigo/Área de Trabalho/PT2_CARBU/ParcelasClientes'
files2 = os.listdir(directory2)

def read_file(file_path) -> list[list[str]]:
    line_list = list()
    with open(file_path, 'r', encoding='latin-1') as file:
        lines =  file.readlines()
        [line_list.append(line.strip().split()) for line in lines if not line.isspace()]
    
    return line_list

def getId() -> int:
    return int(data1[5][1])

def getFinanciado() -> bool:
    return not data1[4][-1] == 'VISTA'

def searchFile() -> str:
    for file in files2:
        id = getId()
        
        pattern = r'\d+'
        matche = re.findall(pattern, file)

        idClient = [int(match) for match in matche]

        if id == idClient[0]:
            return file

    return ''

def getDataAqui() -> list:
        for word in data1[3]:
            pattern = r'^\d{2}/\d{2}/\d{4}$'
        if re.match(pattern, word):
            return [word]
        return ['']


def getValorAqui() -> list:

    for line in data1[1:]:
        if len(line) > 1 and line[1] == "VENDA:":
            return [line[-1]]
        
def getValorParcelas() -> float:
    if not getFinanciado():
        return [0.0]

    line = 20
    try:
        valor = data1[line][-1].replace(',', '.')
        return [float(valor)]
    except:
        return [0.0]
    
def getQtdFinanciamento() -> int:
    try:
        numero = int(''.join(filter(str.isdigit, data1[4][-1])))
        return numero
    except:
        return 0
    
def getValorNominal() -> list:
    i = getQtdFinanciamento()
    if i < 0:
        raise ValueError("O valor de i deve ser não negativo.")

    vetor = []

    for k in range(i + 1):
        termo = int(getValorParcelas()[0]) / (1 + 0.04) ** k
        vetor.append(round(termo, 2))

    return vetor[1:]

def getNome() -> str:
    nome = list()
    stop_re = r'^[0-9]+$'
    for i in reversed(data1[5]):
        nome.insert(0, i)
        if re.match(stop_re, i):
            break
    
    return [' '.join(nome[2:-2])]

def getP() -> str:
    counter: int = 0
    for i, line in enumerate(data1):
        if len(line) == 1:
            counter += 1
        if counter == 3:
            tmp = data1[i-1]
            break

    return [" ".join(tmp[2:5])]

def getDataVencimento() -> str:

        regex_data = r'\b\d{2}/\d{2}/\d{4}\b' 
        datas = []

        for linha in data2[10:]:
            if len(linha) > 2 and not (linha[0].isdigit()):
                if re.match(regex_data, linha[2]):
                    datas.insert(0, linha[2])
                elif re.match(regex_data, linha[1]):
                    datas.insert(0, linha[1])
            elif len(linha) > 2 and (linha[0].isdigit()) and re.match(regex_data, linha[2]):
                datas.insert(0, linha[2])

        return datas[1:]
    
def getValorRecebido() -> list[float]:
    values = list()
    regex_value = r'\b\d{1,5},\d{2}\b'

    for line in data2[11:]:
        for i in range(len(line)):
            if re.match(regex_value, line[i]):
                values.insert(0, line[i+1])
                break
        if len(line) <= 1:
            return values[1:]

for file1 in files1:
    file_path1= os.path.join(directory1, file1)
    data1 = read_file(file_path1)

    file2 = searchFile()
    if file2 != '':    
      file_path2= os.path.join(directory2, file2)
      data2 = read_file(file_path2)
    else:
       continue
            
    dataaquisicao = getDataAqui()
    valoraqui = getValorAqui()
    datavencimento = getDataVencimento()
    valornominal = getValorNominal()
    valorrecebido = getValorRecebido()
    nome = getNome()
    produto = getP()

    tamanhos = [len(dataaquisicao), len(valoraqui), len(datavencimento), len(valornominal), len(valorrecebido), len(nome), len(produto)]

    tamanho_maximo = max(tamanhos)

    dataaquisicao += [None] * (tamanho_maximo - len(dataaquisicao))
    valoraqui += [None] * (tamanho_maximo - len(valoraqui))
    datavencimento += [None] * (tamanho_maximo - len(datavencimento))
    valornominal += [None] * (tamanho_maximo - len(valornominal))
    valorrecebido += [None] * (tamanho_maximo - len(valorrecebido))
    nome += [None] * (tamanho_maximo - len(nome))
    produto += [None] * (tamanho_maximo - len(produto))

    colunas_para_preencher = {
        'Data da Aquisição': dataaquisicao,
        'Valor de Aquisição': valoraqui,
        'Data de Vencimento': datavencimento,
        'Valor Nominal': valornominal,
        'Data do Pagamento Recebido': [None] * tamanho_maximo,
        'Valor do Pagamento Recebido': valorrecebido,
        'Tipo de Ativo': [None] * tamanho_maximo,
        'Cedente': [None] * tamanho_maximo,
        'Sacado': nome,
        'Produto': produto,
    }

    try:
        novos_dados_df = pd.DataFrame(colunas_para_preencher)
        df = pd.concat([df, novos_dados_df], ignore_index=True)
        df.to_excel('novatabela.xlsx', index=False)
        print(df)
    except ValueError as e:
        print(f"Ocorreu um erro: {e}")