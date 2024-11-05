// components/ratingStar/ratingStar.js
Component({
  properties: {
    number: {
      type: Number,
      value: 5,
    },
  },
  data: {
    list: [
      '../../images/star_gray.png',
      '../../images/star_gray.png',
      '../../images/star_gray.png',
      '../../images/star_gray.png',
      '../../images/star_gray.png',
    ],
  },
  lifetimes:{
    attached: function () {
      // 访问属性值
      
      let number = this.data.number;
      console.log(`attach function called number = ${number}`);
      
      // 根据number属性的值来修改list数组
      let list = this.data.list;
      for (let i = 0; i < number; i++) {
        list[i] = '../../images/star_yellow.png';
      }

      // 更新组件数据
      this.setData({
        list
      });
    }
  },
  methods: {

  },
  observers: {
    'number': function(number2) {
      // 在 numberA 或者 numberB 被设置时，执行这个函数
      let number = this.data.number;

      // 根据number属性的值来修改list数组
      let list = this.data.list;
      for (let i = 0; i < number; i++) {
        list[i] = '../../images/star_yellow.png';
      }

      // 更新组件数据
      this.setData({
        list
      });
      console.log("调用了监听函数",number);
    }
  }
});