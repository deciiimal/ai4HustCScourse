//index.js

var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    course0: [],
    feed_length: 0,
    user_info:{},
    defaultImageUrl: "https://gitee.com/c-zxiang/picture/raw/main/计算机组成原理.png",
    onLoad: function() {
      let that = this;
      if (!wx.getStorageSync('token')) {
        // 未登录，跳转到登录页
        wx.reLaunch({
          url: '/pages/login/login'
        });
      } else {
        // 已登录，获取用户信息
        that.setData({
          userInfo: wx.getStorageSync('userInfo')
        });
        const course0 = this.data.course0;
        course0.forEach(item => {
          item['image-url'] = this.data.defaultImageUrl; // 设置默认图片URL
        });
        this.setData({
          course0: course0 // 更新数组
        });
      }
    }

  },
  //事件处理函数
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

  gotoCoursePage: function(event){
    const courseid = event.currentTarget.dataset.courseid; // 从事件对象的dataset中获取courseid
    console.log(`courseid: ${courseid}`);
    wx.navigateTo({
      url: `/pages/course/course?courseid=${courseid}` // 跳转到课程页面并传递courseid
    });
  },

  onLoad: function () {
    console.log('onLoad')
    var that = this
    //调用应用实例的方法获取全局数据
    this.getData();
  },
  upper: function () {
    // wx.showNavigationBarLoading()
    // this.refresh();
    // console.log("upper");
    // setTimeout(function(){wx.hideNavigationBarLoading();wx.stopPullDownRefresh();}, 2000);
  },
  lower: function (e) {
    // wx.showNavigationBarLoading();
    // var that = this;
    // setTimeout(function(){wx.hideNavigationBarLoading();that.nextLoad();}, 1000);
    // console.log("lower")
  },
  //scroll: function (e) {
  //  console.log("scroll")
  //},

  //网络请求数据, 实现首页刷新
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
  getData: function(){
    console.log("loaddata");
    var that = this;
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/course`, // 替换为你的服务器接口地址
      method: 'GET', // 或者 'POST', 根据你的接口要求
      data: {}, // 如果需要，可以在这里传递请求参数
      header: {
        'content-type': 'application/json' // 默认值
        // 可以在这里设置额外的请求头
      },
      success(res) {
        // 请求成功，res是返回的数据
        console.log(res.data.data);
        that.setData({
          course0: res.data.data.course, // 假设返回的数据直接是feed_data
          // feed_length: res.dat // 更新feed_length为请求数据的长度
        });
      },
      fail(error) {
        // 请求失败
        console.error("请求失败：", error);
      }
    });
  },
  refresh: function(){
    wx.showToast({
      title: '刷新中',
      icon: 'loading',
      duration: 3000
    });
    var feed = util.getData2();
    console.log("loaddata");
    var feed_data = feed.data;
    this.setData({
      feed:feed_data,
      feed_length: feed_data.length
    });
    setTimeout(function(){
      wx.showToast({
        title: '刷新成功',
        icon: 'success',
        duration: 2000
      })
    },3000)

  },

  //使用本地 fake 数据实现继续加载效果
  nextLoad: function(){
    wx.showToast({
      title: '加载中',
      icon: 'loading',
      duration: 4000
    })
    var next = util.getNext();
    console.log("continueload");
    var next_data = next.data;
    this.setData({
      feed: this.data.feed.concat(next_data),
      feed_length: this.data.feed_length + next_data.length
    });
    setTimeout(function(){
      wx.showToast({
        title: '加载成功',
        icon: 'success',
        duration: 2000
      })
    },3000)
  }


})
