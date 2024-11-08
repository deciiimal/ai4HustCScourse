// pages/Result/Result.js
Page({
  data: {
    searchCourse: [],
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function(options) {
    const results = options.results;
    // 解码results参数
    const decodedResults = decodeURIComponent(results);
    // 解析results参数
    try {
      const searchResults = JSON.parse(decodedResults);
      console.log('搜索结果：', searchResults);
      // 将搜索结果设置到页面的data中，以便在页面中使用
      this.setData({
        searchCourse: searchResults
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