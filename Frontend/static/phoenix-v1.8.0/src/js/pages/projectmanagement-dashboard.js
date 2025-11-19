import issuesDiscoveredChartInit from '../theme/charts/echarts/issues-discovered-chart';
import zeroBurnOutChartInit from '../theme/charts/echarts/zero-burnout-chart';

const { docReady } = window.phoenix.utils;

docReady(zeroBurnOutChartInit);
docReady(issuesDiscoveredChartInit);
