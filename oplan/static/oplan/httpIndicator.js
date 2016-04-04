angular.module('httpIndicator', [])
.factory('messageBar', function() {
  var self = {
    show: function(className, text, interval) {
      var id = "loadingWidget_" + className;
      if ($('#'+id).length == 0)
        $('<div id="'+id+'" class="messageBar"></div>').prependTo("body");
      $('#'+id).text(text).addClass(className).slideDown();
      if (interval) setInterval(function() { self.hide(className); }, interval);
    },
    hide: function(className) {
      $("#loadingWidget_"+className).slideUp();
    }
  };
  return self;
})
.config(['$httpProvider', '$provide', function ($httpProvider, $provide) {
  $provide.factory('httpIndicatorProvider', function($q, $injector, messageBar, $rootScope) {
    var $http;
		var loading = $("<div class='progressBar'></div>").prependTo("body");
		var timeout;
    var self = {
      // on request start
			'request': function(config) {
        loading.show();
        config.headers.Authorization = 'Basic '+$rootScope.auth;
        return config;
      },

			hideLoader: function() {
			  if(timeout)clearTimeout(timeout);
			  timeout = setTimeout(function() {
            if($http.pendingRequests.length < 1) {
                loading.hide();
            }
						timeout=null;
				}, 200);
			},
			
      // on success
      'response': function(response) {
        $http = $http || $injector.get('$http');
				self.hideLoader();
        console.log("response:",response);
        return response;
      },

      // optional method
      'responseError': function(rejection) {
        $http = $http || $injector.get('$http');
        console.log("HTTP Error: ",rejection);
        self.hideLoader();

        if (rejection.data) {
            messageBar.show("error", "Fehler: " + rejection.data.error, 3000);
        } else if (rejection.status) {
            messageBar.show("error", "Allgemeiner Fehler: " + rejection.status + " " + rejection.statusText, 3000);
        } else {
            messageBar.show("error", "Exception: " + rejection, 3000);
        }
        return $q.reject(rejection);
      }
    };
		return self;
  });

  $httpProvider.interceptors.push('httpIndicatorProvider');
}]);

