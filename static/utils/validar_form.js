$('#validar-form').submit(function () {
    let nome_cpf = $('#search_nome_cpf')
    let data = $('#id_data')
    let erro = $('.alert')

    if (nome_cpf.val() == '' && data.val() == '') {
        erro.removeClass('d-none')
        return false
    }

    return true
})