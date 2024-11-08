//answer.js
var util = require('../../utils/util.js')

var app = getApp()
Page({
  data: {
    motto: '知乎--微信小程序版',
    userInfo_: {},
    comment: {
    },
    like: false,
    like_url: '../../images/gray_heart.png',
    comment_id: 0,

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
    that.getData(commentid);
    this.setData({
      comment_id: commentid,
      userInfo_: wx.getStorageSync('userInfo')
    });
  },
  getData : function(commentid){
    var that = this
    console.log("username logged now: ", wx.getStorageSync('userInfo').username);
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
      },
      fail: function(error) {
        // 请求失败
        console.error("请求失败：", error);
      }
    });
    wx.request({
      url: `http://${app.globalData.ip}:${app.globalData.port}/comment/${commentid}/like`, // 你的服务器接口地址 //记得改！！！
      method: 'GET', // 请求方法，根据实际情况选择'GET'或'POST'
      data: {}, // 如果需要，可以在这里传递请求参数
      header: {
        'content-type': 'application/json', // 默认值
        // 可以在这里设置额外的请求头
        'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
      },
      success: function(res) {
        // 请求成功，res是返回的数据
        console.log(res.data);
        // 这里可以处理返回的数据，例如保存到页面的data中
        that.setData({
          like: res.data.data.liked,
        });
        console.log(that.data.like);
        if(that.data.like === true){
          console.log("called true!");
          that.setData({
            like_url: "../../images/red_heart.png",
          });
        }
        else{
          console.log("called false");
          that.setData({
            like_url: '../../images/gray_heart.png',
          });
        }
      },
      fail: function(error) {
        // 请求失
        console.error("请求失败：", error);
      }
    });
  },
  ChangeLike: function(){
    //如果Like是1 要把like置零 改变路径 同时发送请求
    var that = this;
    console.log(that.data.like);
    if(that.data.like === true){
      that.setData({
        like_url: "../../images/gray_heart.png",
        like: 'false',
      });
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/comment/${that.data.comment_id}/like`,
        method: "DELETE",
        data: {},
        header: {
          'content-type': 'application/json', // 默认值
          // 可以在这里设置额外的请求头
          'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
        },
        success: function(res) {
          console.log("删除成功");
          wx.showToast({
            title: '取消点赞',
            duration:2000,
          })
        },
        fail: function(error) {
          // 请求失败
          console.error("取消失败：", error);
        }

      })
    }
    else{
      that.setData({
        like_url: "../../images/red_heart.png",
        like: 'true',
      });
      wx.request({
        url: `http://${app.globalData.ip}:${app.globalData.port}/comment/${that.data.comment_id}/like`,
        method: "POST",
        data: {},
        header: {
          'content-type': 'application/json', // 默认值
          // 可以在这里设置额外的请求头
          'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
        },
        success: function(res) {
          console.log("点赞成功");
          // console.log(this.like);
          wx.showToast({
            title: '点赞成功',
            duration:2000,
          })
        },
        fail: function(error) {
          // 请求失败
          console.error("点赞失败：", error);
        }

      })
    }
  },
  tapName: function(event){
    console.log(event)
  },
  deleteComment: function(){
    var that = this;
    wx.showModal({
      title: '提示',
      content: '确定要删除该评论吗',
      success (res_) {
        if (res_.confirm) {
          console.log('用户点击确定');
          wx.request({
            url: `http://${app.globalData.ip}:${app.globalData.port}/comment/${that.data.comment_id}`,
            method: "DELETE",
            data: {},
            header: {
              'content-type': 'application/json', // 默认值
              // 可以在这里设置额外的请求头
              'Authorization': "Bearer " + wx.getStorageSync('userInfo').token,
            },
            success: function(res) {
              if(res.statusCode=='200'){
                console.log("删除成功");
                // console.log(this.like);
                wx.showToast({
                  title: '删除成功',
                  duration:2000,
                });
              }
              else if(res.statusCode=='401'){
                console.log("删除失败：",res.statusCode);
                wx.showToast({
                  title: "只能删除自己创建的评论哦~",
                  duration:2000,
                  icon: "none",
                })
              }
              else{
                wx.showToast({
                  title: '删除失败：原因待确认',
                  duration:2000,
                  icon:"none",
                })
              }
            },
            fail: function(error) {
              // 请求失败
              console.error("删除失败：", error);
            }
      
          });
        } else if (res_.cancel) {
          console.log('用户点击取消')
        }
      }
    });
  }
})
