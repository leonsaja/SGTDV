
def validarCpf(cpf):

    if len(cpf) > 11:
        data=cpf.replace('.','').replace('-','')
        
        return data
    elif len(cpf)==11:
        return cpf
    
    return False


def validarCNS(cns):
    cns = ''.join(filter(str.isdigit, str(cns)))
    
    if len(cns) != 15:
        return False
    
    return sum([int(cns[i]) * (15 - i) for i in range(15)]) % 11 == 0


""" def formt_cpf(cpf):
    
    if cpf:
            if len(cpf) == 11:
                return ('{}.{}.{}-{}'.format( cpf[:3], cpf[3:6], cpf[6:9], cpf[9:]))
         """
    
    
    