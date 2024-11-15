//index.js

var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    course0: [],
    feed_length: 0,
    user_info:{},
    defaultImageUrl: "https://gitee.com/c-zxiang/picture/raw/main/计算机组成原理.png",
    researchResult: [],
    loading: false,
    searchKeyword: '',
  },
  onTabItemTap: function(item) {
    console.log('切换 Tab 页:', item.index);  // 输出当前点击的 Tab 页索引

    // 执行页面刷新操作
    this.onLoad();  // 刷新数据
  },
  reloadPage: function () {
    // 显示 loading 弹窗
    this.setData({
      loading: true,
    });

    // 模拟异步操作，假设是重新加载课程数据
    setTimeout(() => {
      this.onLoad(); // 重新加载课程数据
      this.setData({
        loading: false, // 隐藏 loading 弹窗
      });
    }, 1500); // 1.5秒后完成重新加载
  },
  onLoad: function() {
    let that = this;
    if (!wx.getStorageSync('userInfo')) {
      // 未登录，跳转到登录页
      wx.reLaunch({
        url: '/pages/login/login'
      });
    } else {
      console.log('onLoad')
      that.getData();
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
  ChangeLike: function (event) {
    var that = this;
    var courseid = event.currentTarget.dataset.courseid; // 获取传递过来的 courseid
    var courseIndex = event.currentTarget.dataset.idx; // 获取课程在数组中的索引
  
    // 获取当前课程的收藏状态，course0 是课程数据的数组
    var course = that.data.course0[courseIndex];
    console.log("changelike 时候的course0:", that.data.course0);
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
            [`course0[${courseIndex}].liked`]: false, // 更新当前课程的 liked 状态
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
            [`course0[${courseIndex}].liked`]: true, // 更新当前课程的 liked 状态
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
  
  gotoCoursePage: function(event){
    const courseid = event.currentTarget.dataset.courseid; // 从事件对象的dataset中获取courseid
    console.log(`courseid: ${courseid}`);
    wx.navigateTo({
      url: `/pages/course/course?courseid=${courseid}` // 跳转到课程页面并传递courseid
    });
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
  getData: function () {
    var that = this;
    console.log("loaddata");

    wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/course`, // 获取课程列表
        method: 'GET', // 请求方式
        data: {}, // 如果需要，可以在这里传递请求参数
        header: {
            'content-type': 'application/json', // 默认值
            'Authorization': "Bearer " + wx.getStorageSync('userInfo').token, // 用户的 token
        },
        success: function (res) {
            console.log(res.data.data);

            // 获取课程列表
            var courses = res.data.data.course; // 假设返回的数据是课程列表

            // 使用 Promise.all 来保证所有请求完成后再更新数据
            var updatedCourses = [];  // 用于存储更新后的课程数据

            // 遍历每个课程，发起请求获取收藏状态
            var requests = courses.map((item, index) => {
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
                    course0: updatedCourses, // 更新课程列表数据
                });
            }).catch((error) => {
                console.error("获取课程收藏状态时发生错误:", error);
            });
        },
        fail: function (error) {
            console.error("请求课程数据失败：", error);
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
  },
  // 输入内容时触发
onSearchInput: function(e) {
  this.setData({
    searchKeyword: e.detail.value
  });
},

// 搜索功能实现
inputSearch: function() {
  var that = this;
  
  if (!that.data.searchKeyword.trim()) {
    wx.showToast({
      title: '请输入搜索内容',
      icon: 'none',
      duration: 2000
    });
    return;
  }

  wx.showLoading({
    title: '搜索中...',
  });

  wx.request({
    url: `http://${app.globalData.ip}:${app.globalData.port}/search?kw=${that.data.searchKeyword}`,
    method: 'GET',
    data: {
      keyword: that.data.searchKeyword
    },
    header: {
      'content-type': 'application/json',
      'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
    },
    success: function(res) {
      if (res.statusCode === 200) {
        console.log('搜索结果：', res.data);
        
        // 处理搜索结果，根据实际返回数据结构进行相应处理
        that.setData({
          searchResults: res.data.data.course,
        });

        // 如果需要跳转到搜索结果页面
        wx.navigateTo({
          url: '/pages/Result/Result?results=' + encodeURIComponent(JSON.stringify(that.data.searchResults)),
        });
      } else {
        wx.showToast({
          title: '搜索失败',
          icon: 'error',
          duration: 2000
        });
      }
    },
    fail: function(error) {
      console.error('搜索请求失败：', error);
      wx.showToast({
        title: '网络错误',
        icon: 'error',
        duration: 2000
      });
    },
    complete: function() {
      wx.hideLoading();
    }
  });
},


})
