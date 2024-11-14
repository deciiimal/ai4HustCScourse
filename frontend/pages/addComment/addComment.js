// pages/addComment/addComment.js
var app = getApp();
Page({
  data: {
    courseid0: [],
    courseList: ['课程1', '课程2', '课程3', '课程4', '课程5'],
    courseIndex: 0,
    content: '',
    rating: 0
  },
  onLoad: function(){
    var that = this;
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/course`, // 你的服务器接口地址 //记得改！！！
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
        const courseList = res.data.data.course.map(item => item.name);
        const courseid0 = res.data.data.course.map(item=>item.courseid);
        that.setData({
          courseList,
          courseid0,
        });
        console.log(that.data.courseList);
      },
      fail: function(error) {
        // 请求失败
        console.error("课程列表请求失败：", error);
      }
    });
  },
  bindPickerChange : function(e) {
    this.setData({
      courseIndex: e.detail.value
    })
  },

  handleInput : function(e) {
    this.setData({
      content: e.detail.value
    })
  },

  handleStarClick : function(e) {
    const index = e.currentTarget.dataset.index;
    this.setData({
      rating: index + 1
    })
  },

  handleSubmit : function() {
    const { courseid0, courseList, courseIndex, content, rating } = this.data;
    if (!content.trim()) {
      wx.showToast({
        title: '请输入评价内容',
        icon: 'none'
      })
      return;
    }
    if (rating === 0) {
      wx.showToast({
        title: '请选择评分',
        icon: 'none'
      })
      return;
    }
    const dataToPost = {
      courseid: courseid0[courseIndex],
      content: content,
      star: rating,
    };
    console.log(dataToPost);
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/comment/`,
      data: dataToPost,
      method: "POST",
      header: {
        'content-type': 'application/json', // 默认值
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          // 检查是否成功返回了 2xx 状态码
          if (res.data) {
            // 检查业务逻辑是否成功（假设返回的 JSON 中有 `success` 字段）
            wx.showToast({
              title: '评价提交成功',
              icon: 'success'
            });
          } else {
            // 处理业务逻辑错误
            wx.showToast({
              title: '您已提交过评论',
              icon: "error"
            });
          }
        } else {
          // 如果状态码不在 2xx 范围内，认为请求失败
          wx.showToast({
            title: '您已评论过该课程',
            icon: "error"
          });
        }
      },
      fail: (res) => {
        wx.showToast({
          title: '网络请求失败',
          icon: "error"
        });
      },
    });
  }
})