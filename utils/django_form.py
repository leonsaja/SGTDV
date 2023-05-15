
def validarCpf(cpf):

    if len(cpf) > 11:
        data=cpf.replace('.','').replace('-','')
        print('cpf sem ponto',data)
        return data
    
    return False


def validarCNS(cns):
    cns = ''.join(filter(str.isdigit, str(cns)))
    
    if len(cns) != 15:
        return False
    
    return sum([int(cns[i]) * (15 - i) for i in range(15)]) % 11 == 0


   
    
    
    