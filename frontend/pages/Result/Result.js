
var util = require('../../utils/util.js')
var app = getApp()
// pages/Result/Result.js
Page({
  data: {
    searchCourse: [],
  },
  ChangeLike: function (event) {
    var that = this;
    var courseid = event.currentTarget.dataset.courseid; // 获取传递过来的 courseid
    var courseIndex = event.currentTarget.dataset.idx; // 获取课程在数组中的索引
  
    // 获取当前课程的收藏状态，course0 是课程数据的数组
    var course = that.data.searchCourse[courseIndex];
    console.log("changelike 时候的course0:", that.data.searchCourse);
    console.log("course:",courseIndex);
    console.log("course:",course);
    var isLiked = course.liked; // 获取当前课程是否已经被收藏
  
    // 如果已经收藏，点击后要取消收藏
    if (isLiked) {
      // 取消收藏操作
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/course/${courseid}/like`, // 取消收藏的 URL
        method: 'DELETE',
        header: {
          'content-type': 'application/json',
          'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户token
        },
        success: function (res) {
          console.log("取消收藏成功");
          // 更新课程数据
          that.setData({
            [`searchCourse[${courseIndex}].liked`]: false, // 更新当前课程的 liked 状态
          });
          wx.showToast({
            title: '取消收藏成功',
            duration: 2000,
          });
        },
        fail: function (error) {
          console.error("取消收藏失败：", error);
        }
      });
    } else {
      // 添加收藏操作
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/course/${courseid}/like`, // 添加收藏的 URL
        method: 'POST',
        header: {
          'content-type': 'application/json',
          'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户token
        },
        success: function (res) {
          console.log("收藏成功");
          // 更新课程数据
          that.setData({
            [`searchCourse[${courseIndex}].liked`]: true, // 更新当前课程的 liked 状态
          });
          wx.showToast({
            title: '收藏成功',
            duration: 2000,
          });
        },
        fail: function (error) {
          console.error("收藏失败：", error);
        }
      });
    }
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    var that = this;
    const results = options.results;
    // 解码results参数
    const decodedResults = decodeURIComponent(results);
    // 解析results参数
    try {
      const searchResults = JSON.parse(decodedResults);
      console.log('搜索结果：', searchResults);
      var updatedCourses = [];  // 用于存储更新后的课程数据
      var requests = searchResults.map((item, index) => {
        return new Promise((resolve, reject) => {
            // 获取当前课程的收藏状态
            wx.request({
                url: `http://${app.globalData.ip}:${app.globalData.port}/course/${item.courseid}/like`, // 获取收藏状态的接口
                method: 'GET',
                header: {
                    'content-type': 'application/json',
                    'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户的 token
                },
                success: function (likeRes) {
                    console.log(`课程 ${item.courseid} 的收藏状态：`, likeRes.data.data);

                    // 判断返回的收藏状态并更新课程数据
                    if (likeRes.data.data.liked !== undefined) {
                        item.liked = likeRes.data.data.liked; // 假设返回的收藏状态字段为 liked
                        item.like_url = item.liked ? '../../images/red_heart.png' : '../../images/gray_heart.png'; // 更新爱心图标
                    } else {
                        item.liked = false; // 默认设置为未收藏
                        item.like_url = '../../images/gray_heart.png';
                    }

                    // 将更新后的课程项添加到 updatedCourses 中
                    updatedCourses.push(item);
                    resolve();
                },
                fail: function (error) {
                    console.error(`获取课程 ${item.courseid} 收藏状态失败`, error);
                    reject(error);
                }
            });
        });
    });

    // 等待所有请求完成后，更新页面数据
    Promise.all(requests).then(() => {
        updatedCourses.sort((a, b) => a.courseid - b.courseid);
        console.log("所有课程收藏状态已更新:", updatedCourses);
        // 更新页面数据
        that.setData({
          searchCourse: updatedCourses, // 更新课程列表数据
        });
    }).catch((error) => {
        console.error("获取课程收藏状态时发生错误:", error);
    });
    } catch (error) {
      console.error('解析results参数失败：', error);
    }
    // 可以在这里进行其他页面初始化操作
  },
  gotoCoursePage: function(event){
    const courseid = event.currentTarget.dataset.courseid; // 从事件对象的dataset中获取courseid
    console.log(`courseid: ${courseid}`);
    wx.navigateTo({
      url: `/pages/course/course?courseid=${courseid}` // 跳转到课程页面并传递courseid
    });
  },
  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})