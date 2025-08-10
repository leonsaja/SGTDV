document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems);

    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {
        hover: false,
        coverTrigger: false,
        alignment: 'left',
    });
    $('.modal').modal();
    $('.collapsible').collapsible();
    $('select').formSelect();

});
var SPMaskBehavior = function (val) {
    return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
  },
  spOptions = {
    onKeyPress: function(val, e, field, options) {
        field.mask(SPMaskBehavior.apply({}, arguments), options);
      }
  };
  
  

$(function(){
   
    $('.mask-cpf').mask('000.000.000-00', {reverse: true});
    $('.mask-hora').mask('00:00:00');
    $('.mask-data').mask('00/00/0000');
    $('.mask-cep').mask('00000-000');
    $('.mask-telefone').mask(SPMaskBehavior, spOptions);
    $('.mask-celular').mask(SPMaskBehavior, spOptions);
    $('.money2').mask("#.##0,00", {reverse: true});
    $('.money').mask('000,00',{reverse:true});

})
setTimeout(function(){
    $('.show').remove();
},4000);

