$(document).ready(function() {
    twod.start();
    frames.start();
    sp2tx.start();
});

var twod = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/twod";
    twod.socket = new WebSocket(url);
    twod.socket.onmessage = function(event) {
      twod.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    $('img.twod').attr("src", 'data:image/pnjpegg;base64,'+data.src);
  }
};

var frames = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/frames";
    frames.socket = new WebSocket(url);
    frames.socket.onmessage = function(event) {
      frames.process(JSON.parse(event.data));
    }
  },

  process: function(data) {
    console.log(data)
  }
};

var sp2tx = {
  socket: null,
  start: function() {
    var url = "ws://" + location.host + "/sp2tx";
    sp2tx.socket = new WebSocket(url);
    sp2tx.socket.onmessage = function (event) {
      sp2tx.process(event.data);
    }
  },

  process: function(data) {
    console.log("/sp2tx received: " + data);
  }
};
