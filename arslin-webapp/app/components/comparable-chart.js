import Ember from 'ember';

export default Ember.Component.extend({
  chartOptions: {
    chart: {
      type: 'column'
    },
    title: {
      text: 'Vehicle Price Comparison'
    },
    xAxis: {
      type: 'category'
    },
    yAxis: {
      title: {
        text: 'Price'
      }
    },
    legend: {
      enabled: true	
    },
    plotOptions: {
      series: {
        borderWidth: 0,
        dataLabels: {
          enabled: true,
          format: '<a href="{point.url}" target="_blank">${point.y}</a>'
        }
      }
    },
    tooltip: {
      pointFormat: '<span style="color:#222;"><a xlink:href="{point.url}" target="_blank">{point.dealer}</a></span><br>' +
       '<b>${point.y}</b><br>'
    },
  },
});