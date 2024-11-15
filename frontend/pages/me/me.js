//logs.js
var util = require('../../utils/util.js')
var app = getApp()
Page({
  data: {
    navTab: ["收藏课程", "我的评论", "我的点赞", "消息中心"],
    currentNavtab: "0",
    course0: [],
    info: [],
    base64: '',
    myComment: '',
    myLikeComment: {},
    messages: [],
  },
  gotoCoursePage: function(event){
    const courseid = event.currentTarget.dataset.courseid; // 从事件对象的dataset中获取courseid
    console.log(`courseid: ${courseid}`);
    wx.navigateTo({
      url: `/pages/course/course?courseid=${courseid}` // 跳转到课程页面并传递courseid
    });
  },
  gotoSettings: function(){
    wx.navigateTo({
      url: `/pages/setting/setting` // 跳转到课程页面并传递courseid
    });
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
  onTabItemTap: function(item) {
    console.log('切换 Tab 页:', item.index);  // 输出当前点击的 Tab 页索引

    // 执行页面刷新操作
    this.onLoad();  // 刷新数据
  },
  onLoad: function () {
    var that = this;
    console.log("userInfo:", wx.getStorageSync('userInfo'));
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/user/messages`,
      data: {},
      method: "GET",
      header:{
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success:(res)=>{
        that.setData({
          messages: res.data.data.messages
        })
      }
    })
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
            base64: 'data:image/webp;base64,' + res.data.data.image
          })
        }else{
          that.setData({
            base64: "/images/huaxiaoke.jpg"
          })
        }
      }

    })
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
          info: res.data.data,
        })
      }
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
        that.setData({
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
        that.setData({
          myLikeComment: res.data.data.comments,
        })
      },
      fail: (error) => {
        // 处理请求失败的情况
        console.error('请求失败', error);
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/course/my_courses`, // 替换为你的服务器接口地址
      method: 'GET', // 或者 'POST', 根据你的接口要求
      data: {}, // 如果需要，可以在这里传递请求参数
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
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
                            console.log("都进来了");
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
            console.log("所有课程收藏状态已更新:", updatedCourses);
            updatedCourses.sort((a, b) => a.courseid - b.courseid);
            // 更新页面数据
            that.setData({
                course0: updatedCourses, // 更新课程列表数据
            });
        }).catch((error) => {
            console.error("获取课程收藏状态时发生错误:", error);
        });
    },
      fail(error) {
        // 请求失败
        console.error("请求失败：", error);
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
