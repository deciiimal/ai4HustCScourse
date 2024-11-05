//answer.js
var util = require('../../utils/util.js')

var app = getApp()
Page({
  data: {
    motto: '知乎--微信小程序版',
    userInfo: {},
    comment: {
      star:3
    },

  },
  //事件处理函数
  toQuestion: function() {
    wx.navigateTo({
      url: '../question/question'
    })
  },
  onLoad: function (options) {
    console.log('onLoad')
    var that = this
    const commentid = options.commentid
    //调用应用实例的方法获取全局数据
    // app.getUserInfo(function(userInfo){
    //   //更新数据
    //   that.setData({
    //     userInfo:userInfo
    //   })
    // })
    that.getData(commentid);
  },
  getData : function(commentid){
    var that = this
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/comment/${commentid}`, // 你的服务器接口地址 //记得改！！！
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
          comment: res.data.data.comment,
        });

        // console.log(that.data.comment);
      },
      fail: function(error) {
        // 请求失败
        console.error("请求失败：", error);
      }
    });
  },
  tapName: function(event){
    console.log(event)
  }
})
