//logs.js
var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    navTab: ["我的评论", "我的点赞"],
    currentNavtab: "0",
    userName: '',
    myComment: '',
    myLikeComment: {},

  },
  onLoad: function () {
    this.setData({
      userName: wx.getStorageSync('userInfo').username,
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/comment/my_comments`,
      data: {},
      method: "GET",
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success : (res)=>{
        // console.log(res.data);
        this.setData({
          myComment: res.data.data.comments,
        })
      },
      fail: (error) => {
        // 处理请求失败的情况
        console.error('请求失败', error);
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/comment/my_likes`,
      data: {},
      method: "GET",
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success : (res)=>{
        console.log(res.data);
        this.setData({
          myLikeComment: res.data.data.comments,
        })
      },
      fail: (error) => {
        // 处理请求失败的情况
        console.error('请求失败', error);
      }
    });
  },
    /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    const pages = getCurrentPages()
    const perpage = pages[pages.length - 1]
    perpage.onLoad()  
  },

  gotoCommentPage: function(event){
    const commentid = event.currentTarget.dataset.commentid; // 从事件对象的dataset中获取cmtid
    console.log(`commentid: ${commentid}`);
    wx.navigateTo({
      url: `/pages/comment/comment?commentid=${commentid}` // 跳转到课程页面并传递courseid
    });
  },
  logout: function(){
    // 假设你想删除一个名为 'userInfo' 的本地存储项
    wx.removeStorageSync({
      keyList: ['userInfo'],
      success: function () {
        console.log('登出成功');
        wx.showToast({
          title: '登出成功',
          duration:2000,
        })
      },
      fail: function (err) {
        console.error('登出失败', err);
        wx.showToast({
          title: '登出失败 请稍后重试',
          duration:2000,
        })
      }
    });
    wx.reLaunch({
      url: '/pages/login/login',
    })
  },
  switchTab: function(e){
    this.setData({
      currentNavtab: e.currentTarget.dataset.idx
    });
  }
})
