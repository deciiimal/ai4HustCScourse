//discovery.js
var util = require('../../utils/util.js')
var app = getApp()
var wxCharts = require('../../utils/wxcharts.js');
var lineChart = null;
var courseid_g = 0;
Page({
  data: {
    navTab: ["评论", "数据", "GPT"],
    currentNavtab: "0",
    imgUrls: [
      '../../images/24213.jpg',
      '../../images/24280.jpg',
      '../../images/1444983318907-_DSC1826.jpg'
    ],
    indicatorDots: false,
    autoplay: true,
    interval: 5000,
    duration: 1000,
    comment: [],
    feed:[],
    feed_length: 0,
    stats:[],
    textcolor1:'#014f8e',
    textcolor2:'#bfbfbf',
    x_data: ["day1","day2","day3","day4","day5","day6","day7"],
    shoucang: ["1","3","5","4","1","3","2"],
    cmtNum: [12,5,7,4,1,3,5],
    chats: [
      {
        role: 'assistant',
        content: '你好！我是AI助手，有什么可以帮你的吗？'
      }
    ],
    inputMessage: '',
    scrollToMessage: '',
  },
  onLoad: function (options) {
    console.log('onLoad')
    var that = this
    //调用应用实例的方法获取全局数据
    const courseid = options.courseid;
    courseid_g = courseid;
    // this.refresh();
    if (courseid) { // 确保courseid存在
      this.getData(courseid);  //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      console.log(`courseid is ${courseid}`);
    } else {
      console.error('courseid is undefined');
    }

    console.log("attached function called!")
    console.log("x_data: ", this.data.x_data)
    console.log("y_data: ",this.data.shoucang)
    this.OnWxChart(this.data.x_data,this.data.shoucang,'收藏数')
  },
  gotoCommentPage: function(event){
    const commentid = event.currentTarget.dataset.commentid; // 从事件对象的dataset中获取cmtid
    console.log(`commentid: ${commentid}`);
    wx.navigateTo({
      url: `/pages/comment/comment?commentid=${commentid}` // 跳转到课程页面并传递courseid
    });
  },
  getData: function(e){
    // 使用wx.request发送请求
    var that = this;
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/course/${e}/comments`, // 你的服务器接口地址 //记得改！！！
      method: 'GET', // 请求方法，根据实际情况选择'GET'或'POST'
      data: {}, // 如果需要，可以在这里传递请求参数
      header: {
        'content-type': 'application/json' // 默认值
        // 可以在这里设置额外的请求头
      },
      success: function(res) {
        // 请求成功，res是返回的数据
        console.log(res.data);
        // 这里可以处理返回的数据，例如保存到页面的data中
        that.setData({
          comment: res.data.data.comments,
    
        });
        console.log(that.data.comment);
      },
      fail: function(error) {
        // 请求失败
        console.error("课程评论请求失败：", error);
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/course/${e}/stats`,
      method:'GET',
      data:{},
      header: {
        'content-type': 'application/json' // 默认值
        // 可以在这里设置额外的请求头
      },
      success: function(res) {
        // 请求成功，res是返回的数据
        console.log(res.data);
        // 这里可以处理返回的数据，例如保存到页面的data中
        that.setData({
          stats: res.data.data.stats,
        });
        console.log(that.data.stats);
      },
      fail: function(error) {
        // 请求失败
        console.error("统计数据请求失败：", error);
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/chat/${e}`,
      method:'GET',
      data:{},
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success: function(res) {
        console.log(res.data);
        // 将新消息追加到现有消息后面
        const updatedChats = [...that.data.chats, ...res.data.data.messages];
        that.setData({
          chats: updatedChats,
          scrollToMessage: `msg-${updatedChats.length - 1}` // 可选：滚动到最新消息
        });
        console.log(that.data.chats);
      },
      fail: function(error) {
        // 请求失败
        console.error("对话数据请求失败：", error);
      }
    });
  },

  switchTab: function(e){
    this.setData({
      currentNavtab: e.currentTarget.dataset.idx
    });
  },

  bindItemTap: function() {
    wx.navigateTo({
      url: '../answer/answer'
    })
  },
  bindQueTap: function() {
    wx.navigateTo({
      url: '../question/question'
    })
  },
  upper: function () {
    wx.showNavigationBarLoading()
    this.refresh();
    console.log("upper");
    setTimeout(function(){wx.hideNavigationBarLoading();wx.stopPullDownRefresh();}, 2000);
  },
  lower: function (e) {
    wx.showNavigationBarLoading();
    var that = this;
    setTimeout(function(){wx.hideNavigationBarLoading();that.nextLoad();}, 1000);
    console.log("lower")
  },
  //scroll: function (e) {
  //  console.log("scroll")
  //},

  //网络请求数据, 实现刷新
  refresh0: function(){
    var index_api = '';
    util.getData(index_api)
        .then(function(data){
          //this.setData({
          //
          //});
          console.log(data);
        });
  },

  //使用本地 fake 数据实现刷新效果
  refresh: function(){
    var feed = util.getDiscovery();
    console.log("loaddata");
    var feed_data = feed.data;
    this.setData({
      feed:feed_data,
      feed_length: feed_data.length
    });
  },

  //使用本地 fake 数据实现继续加载效果
  nextLoad: function(){
    var next = util.discoveryNext();
    console.log("continueload");
    var next_data = next.data;
    this.setData({
      feed: this.data.feed.concat(next_data),
      feed_length: this.data.feed_length + next_data.length
    });
  },

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
  },

  // 输入框输入事件
  onInput: function(e) {
    this.setData({
      inputMessage: e.detail.value
    });
  },

  // 发送消息
  sendMessage: function() {
    var that = this;
    if (!that.data.inputMessage.trim()) {
      wx.showToast({
        title: '问题不能为空',
        icon: 'error',
        duration: 2000,
      });
      return;
    }
    // 添加用户消息
    const userMessage = {
      message: that.data.inputMessage,
      role: "user",
    };

    let newChats = [...that.data.chats, userMessage];
    let bot_response = {};
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/chat/${courseid_g}`,
      method:'POST',
      data: {
        message: that.data.inputMessage,
      },
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success: function(res) {
        if(res.statusCode == '200'){
          console.log(res.data);
          // bot_response = res.data.data.messages.content;
          // const aiMessage = {
          //   role: 'assistant',
          //   content: bot_response,
          // };
      
          // newChats = [...newChats, aiMessage];
          that.setData({
            inputMessage: '',
          });
          that.onLoad();

        }
        else{
          console.log("出错了!error: ",res.statusCode);
          wx.showToast({
            title: 'error' + res.statusCode,
            icon: "error",
            duration:2000,
          })
        }
      },
      fail: function(error) {
        // 请求失败
        wx.showToast({
          title: '助手开小差了...',
          icon: "none",
          duration:2000,
        })
        console.error("对话请求失败", error);
      }
    })
    // 模拟AI回复
  }
});
