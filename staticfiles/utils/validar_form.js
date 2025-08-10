$('#validar-form').submit(function () {
    let buscar = $('#buscar')
    let data = $('#id_data')
    let erro = $('.alert')
    
    console.log('teste30')

    if (buscar.val() == '' && data.val() == '') {
      erro.removeClass('d-none')
      return false
    }

    return true
  })