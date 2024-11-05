var wxCharts = require('../../utils/wxcharts.js');
var lineChart = null;
Component({
  properties:{

  },
  data:{
    textcolor1:'#014f8e',
    textcolor2:'#bfbfbf',
    x_data: ["day1","day2","day3","day4","day5","day6","day7"],
    shoucang: ["1","3","5","4","1","3","2"],
    cmtNum: [1,3,5,4,1,3,2]
  },
  lifetimes: {
    attached: function () {
      // 组件实例进入页面节点树时执行的生命周期函
      console.log("attached function called!")
      console.log("x_data: ", this.data.x_data)
      console.log("y_data: ",this.data.shoucang)
      this.OnWxChart(this.data.x_data,this.data.shoucang,'收藏数')
    }
  },
  methods:{
    //更换折线图数据为图表一数据
    canvas1_click:function(){
      this.setData({
        textcolor1:'#014f8e',
        textcolor2:'#bfbfbf',
      })  
      //绘制折线图
      this.OnWxChart(this.data.x_data,this.data.shoucang,'收藏数')
    },
    //更换折线图数据为图表二数据
    canvas2_click:function(){
      this.setData({
        textcolor1:'#bfbfbf',
        textcolor2:'#014f8e',
      })
    
      //绘制折线图
      this.OnWxChart(this.data.x_data,this.data.cmtNum,'评论数')
    },
    //图表点击事件
    touchcanvas:function(e){
      lineChart.showToolTip(e, {
        format: function (item, category) {
          return category + ' ' + item.name + ':' + item.data
        }
      });
    },
    //折线图绘制方法
    OnWxChart:function(x_data,y_data,name){
      console.log(name, "chart painted")
      console.log("x_data: ", x_data)
      console.log("y_data: ",y_data)
      var windowWidth = '', windowHeight='';    //定义宽高
      try {
        var res = wx.getWindowInfo();    //试图获取屏幕宽高数据
        windowWidth = res.windowWidth / 750 * 690;   //以设计图750为主进行比例算换
        windowHeight = res.windowWidth / 750 * 550    //以设计图750为主进行比例算换
      } catch (e) {
        console.error('getSystemInfoSync failed!');   //如果获取失败
      }
      lineChart = new wxCharts({
        canvasId: 'lineCanvas',     //输入wxml中canvas的id
        type: 'line',     
        categories:x_data,    //模拟的x轴横坐标参数
        animation: true,  //是否开启动画
      
        series: [{
          name: name,
          data: y_data,
          format: function (val, name) {
            return val + '个';
          }
        }
        ],
        xAxis: {   //是否隐藏x轴分割线
          disableGrid: true,
        },
        yAxis: {      //y轴数据
          title: '',  //标题
          format: function (val) {  //返回数值
            return val.toFixed(2);
          },
          min: 0,   //最小值
          gridColor: '#D8D8D8',
        },
        width: windowWidth*1.1,  //图表展示内容宽度
        height: windowHeight,  //图表展示内容高度
        dataLabel: false,  //是否在图表上直接显示数据
        dataPointShape: true, //是否在图标上显示数据点标志
        extra: {
          lineStyle: 'Broken'  //曲线
        },
      });
    }
  },
  observers: {
    'shoucang': function(shoucang) {
      // 根据number属性的值来修改list数组
      this.OnWxChart(this.data.x_data,this.data.shoucang,'收藏数')
      console.log("调用了收藏数监听函数");
    },
    'cmtNum': function(cmtNum) {
      // 根据number属性的值来修改list数组
      this.OnWxChart(this.data.x_data,this.data.cmtNum,'收藏数')
      console.log("调用了评论数监听函数");
    }
  }

})
