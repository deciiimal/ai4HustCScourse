//app.js
App({
  onLaunch: function () {
    // 小程序启动之后 触发
    let that = this;
    // console.log(wx.getStorageSync('userInfo'));
    if (!wx.getStorageSync('userInfo')) {
      // 未登录，跳转到登录页
      wx.reLaunch({
        url: '/pages/login/login'
      });
    }
    //调用API从本地缓存中获取数据
    var logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    // console.log(wx.getStorageSync('userInfo'));
  },
  // getUserInfo:function(cb){
  //   var that = this
  //   if(this.globalData.userInfo){
  //     typeof cb == "function" && cb(this.globalData.userInfo)
  //   }else{
  //     //调用登录接口
  //     wx.login({
  //       success: function () {
  //         wx.getUserInfo({
  //           success: function (res) {
  //             that.globalData.userInfo = res.userInfo
  //             typeof cb == "function" && cb(that.globalData.userInfo)
  //           }
  //         })
  //       }
  //     })
  //   }
  // },
  globalData:{
    // userInfo:null,
    ip:"127.0.0.1",
    port:"5000",

  }
})