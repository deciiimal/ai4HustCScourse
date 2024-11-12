//index.js
//获取应用实例
const app = getApp()
Page({
  data: {
    username: '',
    password: '',
  },
  //获取输入款内容
  content: function(e){
    this.setData({
      username:e.detail.value
    })
  },
  password: function(e){
    this.setData({
      password:e.detail.value
    })
  },
  //登录事件
  goadmin(){
    let flag = false  //表示账户是否存在,false为初始值
    if(this.data.username=='')
    {
      wx.showToast({
        icon:'none',
        title: '账号不能为空',
      })
    }else if(this.data.password==''){
      wx.showToast({
        icon:'none',
        title: '密码不能为空',
      })
    }else{
      // 构建要发送到服务器的账号和密码数据
      const dataToSend = {
        username: this.data.username,
        password: this.data.password,
      };

      // 向本地服务器发送请求，这里假设你的本地服务器接口为'http://localhost:8080/login'
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/user/login`, // 本地服务器接口地址
        method: 'POST',
        data: dataToSend,
        header: {
          'content-type': 'application/json' // 指定发送的数据类型为JSON
        },
        success: (res) => {
          // 请求成功的处理逻辑
          console.log(res.data); // 打印返回的JSON内容
          if (res.statusCode === 200) {
            // 假设服务器返回的数据结构中，{ success: true, message: '登录成功', token: 'xxx' }
            if (res.data.status == "success") {
              // 假设服务器返回的JSON中包含token，将其保存到本地存储中
              wx.setStorageSync('userInfo', res.data.data);
              // 登录成功后跳转到指定页面
              wx.switchTab({
                url: '/pages/index/index',
              });
              wx.showToast({
                title: "登录成功!",
                icon: 'success',
                duration: 1500
              });
            } else {
              // 服务器返回的错误信息
              wx.showToast({
                title: "error" + res.data.message,
                icon: 'none',
                duration: 2000
              });
            }
          } else {
            // 处理HTTP状态码非200的情况
            wx.showToast({
              title: '服务器错误' + res.statusCode,
              icon: 'none',
              duration: 2000
            });
          }
        },
        fail: (error) => {
          // 请求失败的处理逻辑
          console.error('请求失败：', error);
          wx.showToast({
            title: '请求失败',
            icon: 'none',
            duration: 2000
          });
        }
      })
    } 
  },
  register: function(){
    wx.reLaunch({// 重新启动所有的页面，navigateTo是把新页面加入栈中，可以通过navigate回到原页面
      url: '/pages/register/register',
    })
  }
})
 
