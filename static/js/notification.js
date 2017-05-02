
function notification_list() {
  var x;
    $.ajax({ 
        url: "/tag/notification/",
        type: "POST",
        success: function(data) {
                      var body = data.split(":");
                      var n = 0;
                      while(body[n]){
                          var options = {
                            body: body[n],
                            
                            icon: '/static/image/notification.png',
                            
                            dir : "ltr",
                          };
                          n = n+1;
                          var notification = new Notification("Tag Based File System",options);
                          notification.onclick = function() { 
        window.location.href = '/';
    };
                      }
                     },
        error:function(data) {
                        console.log("Error:"+data.responsetext);
                     },
            });
};

function notifyMe() {
  // Let's check if the browser supports notifications
  if (!("Notification" in window)) {
        alert("This browser does not support desktop notification");
  }

  // Let's check if the user is okay to get some notification
  else if (Notification.permission === "granted") {
          // If it's okay let's create a notification
       notification_list();
  }

  // Otherwise, we need to ask the user for permission
  // Note, Chrome does not implement the permission static property
  // So we have to check for NOT 'denied' instead of 'default'
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      // Whatever the user answers, we make sure we store the information
      if (!('permission' in Notification)) {
        Notification.permission = permission;
      }

      // If the user is okay, let's create a notification
      if (permission === "granted") {
        notification_list();
  }

  // At last, if the user already denied any notification, and you
  // want to be respectful there is no need to bother them any more.
});
}
}