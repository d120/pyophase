angular.module("oplanApp", ["ngRoute", "oplanRaumListe", "oplanTimetable", 
                            "oplanSlot", "oplanBackend", "httpIndicator"])

.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/', {
        templateUrl: 'partials/eile.html',
        controller: 'OplanIndexRedirectCtrl'
      }).
      when('/select_event', {
        title: 'Oplan',
        templateUrl: 'partials/select_veranstaltung.html',
        controller: 'OplanSelectEventCtrl'
      }).
      when('/:vk/home', {
        title: 'Oplan',
        templateUrl: 'partials/home.html',
        controller: 'OplanHomeCtrl'
      }).
      when('/:vk/raumliste', {
        title: 'Raumliste',
        templateUrl: 'partials/raumliste.html',
        controller: 'OplanRaumListeCtrl'
      }).
      when('/:vk/raumliste/tucan', {
        title: 'Raumliste TUCaN-Style',
        templateUrl: 'partials/raumlistetucan.html',
        controller: 'OplanTucanRaumListeCtrl'
      }).
      when('/:vk/raumliste/kleingruppe', {
        title: 'Kleingruppenliste',
        templateUrl: 'partials/kleingruppen.html',
        controller: 'OplanKleingruppenlisteCtrl'
      }).
      when('/:vk/slot/:id', {
        title: 'Slot',
        templateUrl: 'partials/slot.html',
        controller: 'OplanSlotCtrl'
      }).
      when('/:vk/stundenplan/:gruppe', {
        title: 'Stundenplan',
        templateUrl: 'partials/timetable.html',
        controller: 'OplanTimetableCtrl',
        reloadOnSearch: false
      }).
      when('/:vk/raumplan/:raum', {
        title: 'Raumplan',
        templateUrl: 'partials/room.html',
        controller: 'OplanRoomCtrl',
        reloadOnSearch: false
      }).
      otherwise({
        title: '404',
        templateUrl: 'partials/404.html'
        //redirectTo: '/login'
      });
  }])

.run(['$location', '$rootScope', 'oplanHttp', '$routeParams',
  function($location, $rootScope, oplanHttp, $routeParams) {
    $rootScope.$on('$routeChangeSuccess', function (event, current, previous) {
        if (current.$$route) {
          $rootScope.title = current.$$route.title;
          if ($routeParams.vk) $rootScope.vk = $routeParams.vk;
        }
    });
    
    $rootScope.gotoRoomKey = function(e) {
        if (e.keyCode == 13) {
            $location.path("/" + $rootScope.vk + "/raumplan/" + e.target.value).search("w", $rootScope.defaultWeek);
        }
    }

    if (localStorage.auth) {
      $rootScope.auth = localStorage.auth;
    }
    
    oplanHttp.listVeranstaltungen().success(function(result) {
        $rootScope.veranstaltunglist = {}
        result.forEach(function(x) { $rootScope.veranstaltunglist[x.kuerzel] = x; });
        
        $rootScope.$watch('vk', function() {
            if (!$rootScope.vk) return;
            oplanHttp.listStundenplans().success(function(ok) {
                $rootScope.stundenplanlist = ok;      
            });
            $rootScope.defaultWeek = moment($rootScope.veranstaltunglist[$rootScope.vk].start_date).format("YYYY_ww");
        });
        
    });
    
    $rootScope.defaultWeek = "2016_19";
  }])
  
.controller('OplanHomeCtrl', function($scope, $rootScope, oplanHttp) {
    $scope.username = $rootScope.auth ? atob($rootScope.auth).split(/:/)[0] : '';
    $scope.login = function() {
      $rootScope.auth = btoa($scope.username + ":" + $scope.password);
      oplanHttp.doGet("login", {}).then(function(ok) {
        localStorage.auth = $rootScope.auth;
      }, function(err) {
        $rootScope.auth = null;
        setTimeout(function() {
          $("#login_pw").focus().select();
        },1)
      });
      
    }
    $scope.logout = function() {
      $rootScope.auth = null;
      localStorage.auth = "";
    }
    
  })
  
.controller('OplanSelectEventCtrl', function($scope, $rootScope, oplanHttp) {
    
  })

.controller('OplanIndexRedirectCtrl', function($scope, $location, oplanHttp) {
    oplanHttp.listVeranstaltungen().success(function(result) {
        $location.path('/' + result[0].kuerzel + '/home');
    });

  })

.directive('ngRightClick', function($parse) {
    return function(scope, element, attrs) {
        var fn = $parse(attrs.ngRightClick);
        element.bind('contextmenu', function(event) {
            scope.$apply(function() {
                event.preventDefault();
                fn(scope, {$event:event});
            });
        });
    };
})



.factory('mwContextMenu', function($http) {
    return function(event, menuItems) {console.log(event)
        var menu = $("<div class='raumsel'></div>");
        menu.css({ top: event.pageY + "px", left: event.pageX + "px" });
        for(var k in menuItems) {
            var item = $("<div>"+k+"</div>").appendTo(menu);
            item.click(menuItems[k]);
        }
        $(document.body).append(menu);
        setTimeout(function() {
          $(document).one("click", function(e) {
            menu.remove(); e.preventDefault();
          })
          $(document).one("contextmenu", function(e) {
            menu.remove(); e.preventDefault();
          })
        },1)
    }
});
;
