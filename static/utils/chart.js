
function renderiza_faturamento_mensal(url){
    
    fetch(url, {
        method: 'get',
    }).then(function(result){
        return result.json()
    }).then(function(data){

    var ticksStyle = {
      fontColor: '#495057',
      fontStyle: 'bold'
    }
  
    var mode = 'index'
    var intersect = true
  
    var $salesChart = $('#faturamento-diaria')
    
    // eslint-disable-next-line no-unused-vars
    var salesChart = new Chart($salesChart, {
      type: 'bar',
      data: {
        labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'],

      datasets: [
        {
          label: data.labels,

          backgroundColor: '#007bff',
          borderColor: '#007bff',
          data: data.data,
        },
        /* {
          label: "Reembolsos",
          backgroundColor: '#ced4da',
          borderColor: '#ced4da',
          data: [700, 1700, 2700, 2000, 1800, 1500, 2000]
        } */
      ]
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          mode: mode,
          intersect: intersect
        },
        hover: {
          mode: mode,
          intersect: intersect
        },
        legend: {
          display: false
        },
        scales: {
         
          xAxes: [{
            display: true,
            gridLines: {
              display: false
            },
            ticks: ticksStyle
          }]
        }
      }
    })
  

    });
}


/* 
    var $visitorsChart = $('#visitors-chart')
    // eslint-disable-next-line no-unused-vars
    var visitorsChart = new Chart($visitorsChart, {
      data: {
        labels: ['18th', '20th', '22nd', '24th', '26th', '28th', '30th'],
        datasets: [{
          type: 'line',
          data: [100, 120, 170, 167, 180, 177, 160],
          backgroundColor: 'transparent',
          borderColor: '#007bff',
          pointBorderColor: '#007bff',
          pointBackgroundColor: '#007bff',
          fill: false
          // pointHoverBackgroundColor: '#007bff',
          // pointHoverBorderColor    : '#007bff'
        },
        {
          type: 'line',
          data: [60, 80, 70, 67, 80, 77, 100],
          backgroundColor: 'tansparent',
          borderColor: '#ced4da',
          pointBorderColor: '#ced4da',
          pointBackgroundColor: '#ced4da',
          fill: false
          // pointHoverBackgroundColor: '#ced4da',
          // pointHoverBorderColor    : '#ced4da'
        }]
      },
      options: {
        maintainAspectRatio: false,
        tooltips: {
          mode: mode,
          intersect: intersect
        },
        hover: {
          mode: mode,
          intersect: intersect
        },
        legend: {
          display: false
        },
        scales: {
          yAxes: [{
            // display: false,
            gridLines: {
              display: true,
              lineWidth: '4px',
              color: 'rgba(0, 0, 0, .2)',
              zeroLineColor: 'transparent'
            },
            ticks: $.extend({
              beginAtZero: true,
              suggestedMax: 200
            }, ticksStyle)
          }],
          xAxes: [{
            display: true,
            gridLines: {
              display: false
            },
            ticks: ticksStyle
          }]
        }
      }
    })
  })
  
  // lgtm [js/unused-local-variable]
  

    console.log('teste10000')
        const ctx = document.getElementById('faturamento-diaria').getContext('2d');

        new Chart(ctx, {
            type: 'bar',
            data: {
              labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
              datasets: [{
                label: '# of Votes',
                data: [12, 19, 3, 5, 2, 3],
                borderWidth: 1
              }]
            },
            options: {
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }
          }); */
        /* const myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels:['Jan', 'Fev', 'Mar', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'], 
                datasets: [{
                    label: "Gasto em Diaria ",
                   
                    
                }]
            },
           
        }); */
