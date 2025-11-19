(function (factory) {
  typeof define === 'function' && define.amd ? define(factory) :
  factory();
})((function () { 'use strict';

  // import * as echarts from 'echarts';
  const { merge } = window._;

  // form config.js
  const echartSetOption = (chart, userOptions, getDefaultOptions) => {
    const themeController = document.body;
    // Merge user options with lodash
    chart.setOption(merge(getDefaultOptions(), userOptions));

    themeController.addEventListener(
      'clickControl',
      ({ detail: { control } }) => {
        if (control === 'phoenixTheme') {
          chart.setOption(window._.merge(getDefaultOptions(), userOptions));
        }
      }
    );
    
    chart.on('click', params => {  
      console.log(params.seriesType + ',' + params.seriesName + ','+params.name)
     
 
      // Construct the full URL with "id"
      document.location.href = "/tracking/projectsDetails?ty=" +params.seriesType+"&colnm="+params.name+"&chartnm="+params.seriesName;
    })
  };
  // -------------------end config.js--------------------

  const resizeEcharts = () => {
    const $echarts = document.querySelectorAll('[data-echart-responsive]');

    if ($echarts.length > 0) {
      $echarts.forEach(item => {
        const echartInstance = echarts.getInstanceByDom(item);
        echartInstance?.resize();
      });
    }
  };

  const navbarVerticalToggle = document.querySelector('.navbar-vertical-toggle');
  navbarVerticalToggle &&
    navbarVerticalToggle.addEventListener('navbar.vertical.toggle', e => {
      return resizeEcharts();
    });

  // const tooltipFormatter = (params, dateFormatter = 'MMM DD') => {
  //   let tooltipItem = ``;
  //   params.forEach(el => {
  //     tooltipItem += `<div class='ms-1'>
  //       <h6 class="text-700"><span class="fas fa-circle me-1 fs--2" style="color:${
  //         el.borderColor ? el.borderColor : el.color
  //       }"></span>
  //         ${el.seriesName} : ${
  //     typeof el.value === 'object' ? el.value[1] : el.value
  //   }
  //       </h6>
  //     </div>`;
  //   });
  //   return `<div>
  //           <p class='mb-2 text-600'>
  //             ${
  //               window.dayjs(params[0].axisValue).isValid()
  //                 ? window.dayjs(params[0].axisValue).format(dateFormatter)
  //                 : params[0].axisValue
  //             }
  //           </p>
  //           ${tooltipItem}
  //         </div>`;
  // };

  // dayjs.extend(advancedFormat);

  /* -------------------------------------------------------------------------- */
  /*                             Echarts Total Sales                            */
  /* -------------------------------------------------------------------------- */

  const issuesDiscoveredChartInit = () => {
    const { getColor, getData, resize } = window.phoenix.utils;
    const issuesDiscoveredChartEl = document.querySelector('.echart-issue-chart');

    if (issuesDiscoveredChartEl) {
      const userOptions = getData(issuesDiscoveredChartEl, 'echarts');
      const chart = window.echarts.init(issuesDiscoveredChartEl);

      const getDefaultOptions = () => ({
        color: [
          getColor('info'),
          getColor('info-300'),
          getColor('warning-300'),
          getColor('danger-300'),
          getColor('success-300'),
          getColor('primary')
        ],
        tooltip: {
          trigger: 'item'
        },
        responsive: true,
        maintainAspectRatio: false,

        series: [
          {
            name: '',
            type: 'pie',
            radius: ['48%', '90%'],
            startAngle: 30,
            avoidLabelOverlap: false,
            // label: {
            //   show: false,
            //   position: 'center'
            // },

            label: {
              show: false,
              position: 'center',
              formatter: '{x|{d}%} \n {y|{b}}',
              rich: {
                x: {
                  fontSize: 31.25,
                  fontWeight: 800,
                  color: getColor('gray-700'),
                  padding: [0, 0, 5, 15]
                },
                y: {
                  fontSize: 12.8,
                  color: getColor('gray-700'),
                  fontWeight: 600
                }
              }
            },
            emphasis: {
              label: {
                show: true
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 7, name: 'Decommissioned' },
              { value: 3, name: 'Governance Review' },
              { value: 1, name: 'In Annual Review' },
              { value: 2, name: 'In Development' },
              { value: 1, name: 'Legacy' },
              { value: 16, name: 'Validated' }
            ]
          }
        ],
        grid: {
          bottom: 0,
          top: 0,
          left: 0,
          right: 0,
          containLabel: false
        }
      });

      echartSetOption(chart, userOptions, getDefaultOptions);

      resize(() => {
        chart.resize();
      });
    }
  };

  /* -------------------------------------------------------------------------- */
  /*                             Echarts Total Sales                            */
  /* -------------------------------------------------------------------------- */

  const zeroBurnOutChartInit = () => {
    const { getColor, getData, resize, getPastDates } = window.phoenix.utils;
    const $zeroBurnOutChartEl = document.querySelector(
      '.echart-zero-burnout-chart'
    );

    const $zeroBurnOutChartE2 = document.querySelector(
      '.echart-zero-burnout-chart2'
    );

    const $zeroBurnOutChartE3 = document.querySelector(
      '.echart-zero-burnout-chart3'
    );

    if ($zeroBurnOutChartEl) {
      const userOptions = getData($zeroBurnOutChartEl, 'echarts');
      const chart = window.echarts.init($zeroBurnOutChartEl);

      const getDefaultOptions = () => ({
        color: [  
          getColor('info'),
          getColor('warning')
        ],
        tooltip: {
          trigger: 'item',
          // backgroundColor: getColor('gray-soft'),
          // borderColor: getColor('gray-200'),
          // formatter: params => tooltipFormatter(params, 'MMM DD, YYYY'),
          // axisPointer: {
          //   shadowStyle: {
          //     color: 'red'
          //   }
          // }
        }, 
        xAxis: {
          type: 'category',
          data: ['High', 'Low', 'Medium', 'None'],
          triggerEvent: true
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name:'Model Risk Tier',
            data: [3, 1, 7, 19],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ],
        grid: {
          right: 5,
          left: 0,
          bottom: '15%',
          top: 20,
          containLabel: true
        }
      });

      echartSetOption(chart, userOptions, getDefaultOptions);

      resize(() => {
        chart.resize();
      });
    }

    if ($zeroBurnOutChartE2) {
      const userOptions = getData($zeroBurnOutChartE2, 'echarts');
      const chart2 = window.echarts.init($zeroBurnOutChartE2);

      const getDefaultOptions = () => ({
        color: [  
          getColor('info'),
          getColor('warning')
        ],
        tooltip: {
          trigger: 'item',
          // backgroundColor: getColor('gray-soft'),
          // borderColor: getColor('gray-200'),
          // formatter: params => tooltipFormatter(params, 'MMM DD, YYYY'),
          // axisPointer: {
          //   shadowStyle: {
          //     color: 'red'
          //   }
          // }
        }, 
        xAxis: {
          type: 'category',
          data: ['High', 'Low', 'Medium', 'None'],
          triggerEvent: true
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name:'Materiality',
            data: [6, 4, 2, 18],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ],
        grid: {
          right: 5,
          left: 0,
          bottom: '15%',
          top: 20,
          containLabel: true
        }
      });

      echartSetOption(chart2, userOptions, getDefaultOptions);

      resize(() => {
        chart2.resize();
      });
    }

    if ($zeroBurnOutChartE3) {
      const userOptions = getData($zeroBurnOutChartE3, 'echarts');
      const chart3 = window.echarts.init($zeroBurnOutChartE3);

      const getDefaultOptions = () => ({
        color: [  
          getColor('info'),
          getColor('warning')
        ],
        tooltip: {
          trigger: 'item',
          // backgroundColor: getColor('gray-soft'),
          // borderColor: getColor('gray-200'),
          // formatter: params => tooltipFormatter(params, 'MMM DD, YYYY'),
          // axisPointer: {
          //   shadowStyle: {
          //     color: 'red'
          //   }
          // }
        }, 
        xAxis: {
          
          type: 'category',
          data: ['Approved', 'Approved with Finding', 'Not Approved'],
          triggerEvent: true
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name:'Approval Status',
            data: [13, 8, 9],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ],
        grid: {
          right: 5,
          left: 0,
          bottom: '15%',
          top: 20,
          containLabel: true
        }
      });

      echartSetOption(chart3, userOptions, getDefaultOptions);

      resize(() => {
        chart3.resize();
      });
    }
  };

  const { docReady } = window.phoenix.utils;

  docReady(zeroBurnOutChartInit);
  docReady(issuesDiscoveredChartInit);

}));
//# sourceMappingURL=projectmanagement-dashboard.js.map
