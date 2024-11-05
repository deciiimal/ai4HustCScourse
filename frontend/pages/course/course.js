//discovery.js
var util = require('../../utils/util.js')
var app = getApp()
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
  },
  onLoad: function (options) {
    console.log('onLoad')
    var that = this
    //调用应用实例的方法获取全局数据
    const courseid = options.courseid;
    // this.refresh();
    if (courseid) { // 确保courseid存在
      this.getData(courseid);  //!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      console.log(`courseid is ${courseid}`);
    } else {
      console.error('courseid is undefined');
    }
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
        console.error("请求失败：", error);
      }
    });
    wx.request({
      url: '',
    })

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
  }
});
