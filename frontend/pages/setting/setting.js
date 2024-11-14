var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    userInfo: {
      userid: '123456',
      username: 'john_doe',
      email: 'john@example.com'
    },
    showAvatarModal: false,
    base64: '',//真实头像
    show: '',// 用于展示
    avatarBase64: '',//临时存储base64值
    showModal: false,  // 控制修改用户信息的弹窗显示
    showPasswordModal: false,  // 控制修改密码的弹窗显示
    modalType: '',  // 弹窗的类型：userid, username, email
    modalInput: '',  // 弹窗输入框的内容
    oldPassword: '', // 输入的原密码
    newPassword: '', // 输入的新密码
    confirmNewPassword: '' // 输入的确认新密码
  },

  onLoad(){
    var that = this;
    
    
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/user/me`,
      data: {},
      method: "GET",
      header:{
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success:(res)=>{
        const date = new Date(res.data.data.create_at);
        res.data.data.create_at = date.toLocaleString('en-GB', {
          weekday: 'short', // 可以省略，这里用来获取类似 "Wed" 的星期格式
          day: '2-digit',
          month: 'short',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        });
        that.setData({
          userInfo: res.data.data,
        })
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/avatar/d/${wx.getStorageSync('userInfo').userid}`,
      data: {},
      method: "GET",
      header:{
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success:(res)=>{
        if(res.statusCode == 200){
          that.setData({
            base64: 'data:image/webp;base64,' + res.data.data.image,
            show: 'data:image/webp;base64,' + res.data.data.image
          }) 
        }else{
          that.setData({
            show: "/images/huaxiaoke.png"
          })
        }
      }
    })
  },
  // 修改用户信息（用户名、邮箱、用户ID）
  modifyUserInfo(e) {
    const type = e.currentTarget.dataset.type;
    this.setData({
      showModal: true,
      modalType: type,  // 记录弹窗的类型
      modalInput: this.data.userInfo[type]  // 默认填入当前值
    });
  },

  // 关闭修改用户信息的弹窗
  closeModal() {
    this.setData({
      showModal: false
    });
  },

  // 处理输入框的变化
  onInputChange(e) {
    this.setData({
      modalInput: e.detail.value
    });
  },
  modifyAvatar() {
    this.setData({
      showAvatarModal: true
    });
  },
  chooseAvatar() {
    wx.chooseMedia({
      count: 1, // 只选择一个文件
      mediaType: ['image'], // 只允许选择图片
      success: (res) => {
        // 获取选择的文件路径
        const filePath = res.tempFiles[0].tempFilePath;
  
        // 检查文件是否是 .jpg 或 .png 格式
        const fileExtension = filePath.split('.').pop().toLowerCase();
        if (fileExtension === 'png') {
          wx.getFileSystemManager().readFile({
            filePath: filePath,
            encoding: 'base64',
            success: (res) => {
              // 设置头像的 Base64 数据
              this.setData({
                base64: 'data:image/png;base64,' + res.data,
                avatarBase64: res.data
              });
            }
          });
        } else {
          wx.showToast({
            title: '请上传 .jpg 或 .png 格式的图片',
            icon: 'none'
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '图片选择失败',
          icon: 'none'
        });
      }
    });
  },
  
  closeAvatarModal() {
    this.setData({
      showAvatarModal: false,
      avatarBase64: '', // 重置图片
    });
  },  
  // 确认修改用户信息
  confirmModification() {
    var that = this;
    const { modalType, modalInput, userInfo } = that.data;

    // 检查输入是否有更改
    if (modalInput !== userInfo[modalType]) {
      var data1 = {'email':modalInput};
      if(modalType == 'username') data1 = {'username':modalInput};
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/user/${modalType}`,
        method: 'PUT',
        data: data1,
        header: {
          'content-type': 'application/json',
          'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户token
        },
        success: function (res) {
          if(res.statusCode==200){
            userInfo[modalType] = modalInput;
            wx.showToast({
            title: '修改成功',
            duration: 2000,
          });
          that.setData({
            userInfo : userInfo,
            showModal: false
          });
          that.onLoad();
          }
          else{
            wx.showToast({
              title: '修改失败',
              icon: 'error',
              duration: 2000,
            });
          }
        },
        fail: function (error) {
          console.error("网络错误");
        }
      });
      that.setData({
        showModal: false
      });
    } else {
      wx.showToast({
        title: '未做任何修改',
        icon: 'none'
      });
    }
  },

  // 修改密码
  modifyPassword() {
    this.setData({
      showPasswordModal: true
    });
  },

  // 关闭修改密码的弹窗
  closePasswordModal() {
    this.setData({
      showPasswordModal: false
    });
  },

  // 处理原密码输入
  onOldPasswordInput(e) {
    this.setData({
      oldPassword: e.detail.value
    });
  },

  // 处理新密码输入
  onNewPasswordInput(e) {
    this.setData({
      newPassword: e.detail.value
    });
  },

  // 处理确认新密码输入
  onConfirmNewPasswordInput(e) {
    this.setData({
      confirmNewPassword: e.detail.value
    });
  },

  // 确认修改密码
  confirmPasswordModification() {
    var that = this;
    const { oldPassword, newPassword, confirmNewPassword } = that.data;

    if (newPassword !== confirmNewPassword) {
      wx.showToast({
        title: '两次密码不一致',
        icon: 'none'
      });
      return;
    }

    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/user/password`,
      method: 'PUT',
      data: {
        'old_password': oldPassword,
        'new_password': newPassword,
        'confirm_password': confirmNewPassword
      },
      header: {
        'content-type': 'application/json',
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户token
      },
      success: function (res) {
        if(res.statusCode==200){
          wx.showToast({
          title: '修改成功',
          duration: 2000,
        });
        that.setData({
          showPasswordModal: false
        });
        }
        else{
          wx.showToast({
            title: '修改失败',
            icon: 'error',
            duration: 2000,
          });
        }
      },
      fail: function (error) {
        console.error("网络错误");
      }
    });
  },
  confirmAvatarModification() {
    const avatarData = this.data.avatarBase64;
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/avatar`,
      method: 'POST',
      header: {
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
        'content-type': 'application/json',
      },
      data: {
        'image': avatarData,
      },
      success: (res) => {
        if (res.statusCode == 200) {
          this.setData({
            show: this.data.base64,
            avatarBase64: null,
            showAvatarModal: false, // 关闭弹窗
          });
          wx.showToast({
            title: '头像修改成功',
            icon: 'success',
          });
        } else {
          wx.showToast({
            title: '头像修改失败',
            icon: 'none',
          });
        }
      },
      fail: () => {
        wx.showToast({
          title: '网络异常',
          icon: 'none',
        });
      }
    });
  },
  
  // 登出
  logout() {
    // 清除用户信息，跳转到登录页面
    wx.removeStorageSync('userInfo');
    wx.reLaunch({
      url: '/pages/login/login'
    });
  }
});
