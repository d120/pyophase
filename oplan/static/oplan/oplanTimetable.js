angular.module('oplanTimetable', ['ui.calendar'])

.controller('OplanTimetableCtrl', ['$scope', '$routeParams', 'oplanHttp', 'uiCalendarConfig', '$location', '$interval', 'messageBar', '$window',
  function($scope, $routeParams, oplanHttp, uiCalendarConfig, $location, $interval, messageBar, $window) {
    $scope.gruppe = $routeParams.gruppe;
    /* config object */
    $scope.calendar = {
        height: $($window).height() - 70,
        firstDay: 1,
        weekNumbers: true,
        editable: true,
        scrollTime: '07:30:00',
        timeFormat: 'H:mm',
        snapDuration: '0:05',
        defaultView: 'agendaWeek',
        selectable: true,
        selectHelper: true,
        select: onSelectTimerange,
        eventDrop: onEventChange,
        eventResize: onEventChange,
        header:{
          left: 'agendaWeek agendaDay',
          center: 'title',
          right: 'today prev,next'
        },
        viewRender: onRenderView,
        eventClick: onEventClick
    };
    
    angular.element($window).on('resize', function() {
        $scope.calendar.height = $($window).height() - 80;
        $scope.$apply();
    })

    function onRenderView(view, element) {
        $scope.woche = view.start.format("YYYY_ww");
        $location.search("w", $scope.woche).replace();
    }
    
    function onSelectTimerange(start, end) {
        var desc = prompt("Termin von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" eintragen?\n\nKurztitel:");
        if (desc === null) return;
        
        oplanHttp.newTermin(start, end, desc, $scope.gruppe)
        .success(function() {
            uiCalendarConfig.calendars.timetable.fullCalendar('unselect');
            uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
        })
        .error(function(data) {
            alert("Allgemeiner Fehler");
        });
    }
    
    function onEventChange(event, delta, revertFunc, jsEvent, ui, view ) {
        oplanHttp.moveTermin(event.id, event.start, event.end, true)
        .success(function(data) {
            uiCalendarConfig.calendars.timetable.fullCalendar('unselect');
            uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
            messageBar.show('success', ''+data.modifications+' Einträge verschoben', 1500);
        })
        .error(function(data) {
            revertFunc();
        });
    }

    function onEventClick(event, jsEvent, view) {
        $scope.slotId = event.id;
    }
    
    $scope.closeDetails = function() {
        $scope.slotId = null;
    }
    
    function eventLoader (start, end, timezone, callback) {
      oplanHttp.doGet("stundenplan", { format: "json", w: moment(start).format("YYYY_WW"), g: $routeParams.gruppe })
      .success(function(result) {
        
        callback(result.map(function(x) {
          x.start = new Date(x.von.replace(/ /,'T'));
          x.end = new Date(x.bis.replace(/ /,'T'));
          if (x.typ == 'ok') x.color = 'green';
          if (x.min_platz < 1) { x.title = x.kurztitel; x.color = '#808080'; }
          else x.title = x.kurztitel + ' (' + x.anz + ')';
          return x;
        }));
      });
    }
    
    $scope.eventSources = [ eventLoader ];
    
    if ($routeParams.w) {
      var paramDate = $routeParams.w.split(/_/);
      var d = moment().year(paramDate[0]).date(1).month(1).isoWeek(paramDate[1]-1).day("Monday");
      $scope.calendar.defaultDate = d;
    }
    
  }])
  
  
  
.controller('OplanRoomCtrl', ['$scope', '$routeParams', 'oplanHttp', 'uiCalendarConfig', '$location', 'messageBar', '$window', 'mwContextMenu',
  function($scope, $routeParams, oplanHttp, uiCalendarConfig, $location, messageBar, $window, mwContextMenu) {
    $scope.room = $routeParams.raum;
    /* config object */
    $scope.calendar = {
        height: $($window).height() - 80,
        firstDay: 1,
        weekNumbers: true,
        editable: true,
        scrollTime: '07:30:00',
        timeFormat: 'H:mm',
        snapDuration: '0:05',
        defaultView: 'agendaWeek',
        selectable: true,
        selectHelper: true,
        select: onSelectTimerange,
        eventDrop: onEventChange,
        eventResize: onEventChange,
        header:{
          left: 'agendaWeek agendaDay',
          center: 'title',
          right: 'today prev,next'
        },
        viewRender: onRenderView,
        eventClick: onEventClick,
        eventRender: onEventRender
    };
    
    function onRenderView(view, element) {
        $location.search("w", view.start.format("YYYY_ww")).replace();
        $scope.calStart = view.start.toDate();
    }
    
    var lastDesc = "";
    function onSelectTimerange(start, end) {
        var desc = prompt("Eintragen, dass "+$scope.room+" von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" frei ist?\n\nKommentar:", lastDesc);
        if (desc === null) return;
        lastDesc = desc;
        
        oplanHttp.setRaumFrei(null, $scope.room, start, end, desc, "???")
        .success(function() {
            uiCalendarConfig.calendars.timetable.fullCalendar('unselect');
            uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
        })
        .error(function(data) {
            uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
        });
    }
    
    function onEventRender(event, element) {
      element.contextmenu(function(e) {
        e.preventDefault();
        if (event.startEditable) {
          mwContextMenu(e, {
            "Bearbeiten": function() {
              onEventChange(event, 0, function(){}, e, null, null);
            },
            "Löschen": function() {
              if (confirm("Löschen?")) {
                oplanHttp.deleteRaumFrei(event.id).success(function() {
                  uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
                });
              } else {
                revertFunc();
              }
            }
          })
          
        }
      });
    }
    function onEventClick(event, jsEvent, view) {
      
    }
    function onEventChange(event, delta, revertFunc, jsEvent, ui, view ) {
      if (event.typ == "frei") {
        setTimeout(function() {
            var desc = prompt("Raum-Frei-Eintragung ändern? Raum: "+$scope.room+" von "+event.start.format("HH:mm")+" bis "+event.end.format("HH:mm")+"\n\nKommentar:", event.title);
            if (desc === null) { revertFunc(); return; }
            
            oplanHttp.setRaumFrei(event.id, $scope.room, event.start, event.end, desc, "???")
            .success(function() {
                uiCalendarConfig.calendars.timetable.fullCalendar('unselect');
                uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');

            })
            .error(function(data) {
                revertFunc();
            });
        },1);
      }
    }

    
    function eventLoader (start, end, timezone, callback) {
      oplanHttp.doGet("stundenplan", { format: "json", w: moment(start).format("YYYY_WW"), raum: $routeParams.raum })
      .success(function(result) {
        
        callback(result.map(function(x) {
          x.start = new Date(x.von);
          x.end = new Date(x.bis);
          x.title = x.kommentar;
          var edit = false;
          switch(x.typ) {
            case "ok": x.color = "darkgreen"; break;
            case "wunsch": x.color = "orange"; break;
            case "frei": x.color = "#22ee55"; x.textColor="green";
             if(x.status!="tucan") edit=true;
             break;
            case "block": x.color = "red"; x.rendering="background"; break;
              break;
          }
          x.startEditable=edit; x.durationEditable=edit;
          return x;
        }));
      });
    }
    
    $scope.eventSources = [ eventLoader ];
    
    if ($routeParams.w) {
      var paramDate = $routeParams.w.split(/_/);
      var d = moment().year(paramDate[0]).date(1).month(1).isoWeek(paramDate[1]-1).day("Monday");
      $scope.calendar.defaultDate = d;
    }
    
    oplanHttp.doGet("raum", { nummer: $scope.room })
    .success(function(data) {
        $scope.raumInfo = data.info;
    });
    
    oplanHttp.doGet('raum', { all: '1' })
    .success(function(data) {
        $scope.raumliste = data.raumliste;
        setTimeout(function() {
        		// PFUI !
        		// das geht bestimmt sauber mit einer directive...
        		var scrollTop = $("#sidebar .current").position().top; console.log(scrollTop);
        		$("#sidebar")[0].scrollTop = Math.max(scrollTop-100,0);
        }, 100);
    });

    $scope.updateAusVerw = function() {
        oplanHttp.doPost("parse_timetable.php", { start: $scope.calStart.getTime()/1000, 
          nummer: $scope.room })
        .success(function(data) {
          if(data.success) {
              uiCalendarConfig.calendars.timetable.fullCalendar('refetchEvents');
          } else {
              alert(data.error);
          }
        })
        .error(function(data) {
            alert("Allgemeiner Fehler");
        });
    }
    
  }])
;
