
//==>
//==> MessageBar helper

function MessageBar() {
    this.show = function(className, text, interval, isHtml) {
      var id = "loadingWidget_" + className;
      if ($('#'+id).length == 0)
        $('<div id="'+id+'" class="messageBar"></div>').prependTo("body").click(function(){messageBar.hide(className)});
      var $el = $('#'+id);
      if (isHtml) $el.html(text); else $el.text(text);
      $el.addClass(className).slideDown();
      if (interval) setInterval(function() { messageBar.hide(className); }, interval);
    };
    this.hide = function(className) {
      $("#loadingWidget_"+className).slideUp();
    };
    var loading = $("<div class='progressBar'></div>").prependTo("body").hide();

    $(document).ajaxStart(function() {
        loading.show();
    });
    $(document).ajaxStop(function() {
        loading.hide();
    });
    $(document).ajaxError(function(event, jqxhr, settings, thrownError) {
        console.log("ajaxError",event,jqxhr,thrownError);
        if (event.data) {
            messageBar.show("error", "Fehler: " + event.data.error, 3000);
        } else if (jqxhr.status) {
            messageBar.show("error", "Allgemeiner Fehler: " + jqxhr.status + " " + jqxhr.statusText, 3000);
        } else {
            messageBar.show("error", "Exception: " + thrownError, 3000);
        }
    });

};

//==>
//==> Context menu helper

function ShowContextMenu(event, menuItems) {
    $(".ddmenu.context").remove();
    var menu = $("<div class='ddmenu context'></div>");
    for(var k in menuItems) {
        var item = $("<div>"+k+"</div>").appendTo(menu);
        item.click(menuItems[k]);
    }
    $(document.body).append(menu);
    var x = event.pageX, y = event.pageY, xx = menu.width(), yy = menu.outerHeight();
    if (x+xx > window.innerWidth) x -= xx;
    if (y+yy > window.innerHeight) y -= yy;

    menu.css({ top: y + "px", left: x + "px" }).slideDown();
    setTimeout(function() {
      $(document).one("click", function(e) {
        menu.remove(); e.preventDefault();
      })
      $(document).one("contextmenu", function(e) {
        menu.remove(); e.preventDefault();
      })
    },1)
}
function CloseContextMenu(event, menuItems) {
    $(".ddmenu.context").remove();
}


//==>
//==> make new stuff red
// Converts a #ffffff hex string into an [r,g,b] array
var h2r = function(hex) {
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if( result ) return [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16)
    ];
    var result = /^rgb\(([\d]+),\s*([\d]+),\s*([\d]+)\)$/i.exec(hex);
    if( result ) return [
        parseInt(result[1], 10),
        parseInt(result[2], 10),
        parseInt(result[3], 10)
    ];
    return null;
};
var _interpolateColor = function(color1, color2, factor) {
  if (arguments.length < 3) { factor = 0.5; }
  var result = color1.slice();
  for (var i=0;i<3;i++) {
    result[i] = Math.round(result[i] + factor*(color2[i]-color1[i]));
  }
  return result;
};
function make_new_stuff_red($el) {
    var age = parseInt($el.attr("data-age"));
    var oldAge = parseInt($el.attr("data-old"));
    if (!oldAge) oldAge = 21600;
    var curColorAttr = $el.css("background-color");
    var curColor = h2r(curColorAttr);
    var redColor = [255,0,0];
    //TODO var newColor = _interpolateColor(curColor, redColor, Math.max(0, age - oldAge)
}
function newRandomBarcode(){
    code = "" + (Math.floor(Math.random()*999999)+2000000);

    weighed_sum = parseInt(code[0])*3 + parseInt(code[1])*1 + parseInt(code[2])*3 +
        parseInt(code[3])*1 + parseInt(code[4])*3 + parseInt(code[5])*1 + parseInt(code[6])*3;
    checksum = (10 - (weighed_sum % 10)) % 10;
    code = "" + code + checksum;
    return code;
}

//==>
//==> Startup Code OPLAN

$(function() {
    window.messageBar = new MessageBar();
    function ddlink_open(e) {
        var targetSel = $(this).attr("data-target");
        if (targetSel == "#raumliste" && !$("#raumliste").length) {
            var $lst = $("<div id=raumliste class=ddmenu></div>").appendTo(this);
            $.get("/plan/api/room/?visible="+oplan.is_staff, function(rooms) {
                rooms.forEach(function(room) {
                    $lst.append(
                        (oplan.is_staff=="True" ? "<a class='right' href='/admin/oplan/room/"+escape(room.id)+"/change/'>(edit)</a> ":"") +
                        "<a href='/plan/roomcalendar/"+escape(room.number)+"'>"+room.number+"</a> " +
                        "");
                });
            });
        }
        $(targetSel).css({'left': $(this).offset().left, 'display': 'block'});
        return false;
    }
    function ddlink_close() {
        var targetSel = $(this).attr("data-target");
        $(targetSel).hide();
    }
    if (!('ontouchstart' in window))
        $(".menuddlink").mouseenter(ddlink_open).mouseleave(ddlink_close);

    //$("[data-age]").each(make_new_stuff_red);
    $("#kdvuserbarcode_set-group .add-row a").click(function() {
        $(".dynamic-kdvuserbarcode_set").last().find(".field-code input.vTextField").val(
            newRandomBarcode());
    });

    $("#oplan").on('mouseenter', '.fc-event', function(e) {
        var eventObj = $(this).data("event");
        if (!eventObj) eventObj = $(this).data("fcSeg").event;
        console.log("dom item: ",this);
        console.log("event: ",eventObj);

        var $h   = $("#hoverhelp");
        if ($h.length == 0) {
            $h=$("<div id=hoverhelp style='position:fixed;background:white;right:5px;top:60px;border:1px solid black'><b></b><br><span></span></div>").appendTo("body");
        }
        $h.find("b").text(eventObj.title);
        $h.find("span").text(eventObj.constraints_freetext);
        $h.show();



    });
});

function calendarDefaultOptions(extendOptions) {
    return $.extend({
        schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',

        timezone: 'local',
        allDaySlot: false,

        lang: 'de',
        views: {
            timelineDay: { titleFormat: 'dddd DD.MM.YYYY' },
            agendaDay: { titleFormat: 'dddd DD.MM.YYYY' },
        },
        buttonText: { timelineDay: 'Tag quer', agendaDay: 'Tag lÃ¤ngs' },

        defaultDate: localStorage.calendarDate,

        editable: true,
        droppable: true, // this allows things to be dropped onto the calendar
        selectable: true,
        selectHelper: true,

        firstDay: 1,
        businessHours:{
            start: '09:00', end: '19:00',
            dow: [ 4,5,6,7]
        },

        drop: function() {
            $(this).remove();  //  remove the element from the "Draggable Events" list
        },

    }, extendOptions);
}

function getEventContextMenu(event, jsEvent) {
    var menu = {};
    if (event.view_url) {
        menu["Detailansicht"] = function() {
            location = event.view_url;
        };
    }
    if (event.termin_id) {
        menu["Als interessant markieren"] = function() {
            alert("foobar");
        };
    }
    if (oplan.mode != "akreadonly") {
        menu["Bearbeiten"] = function() {
            window.open(event.edit_url+"?_popup=1", "", "width=800,height=600,scrollbars=yes");
        };
        if (event.termin_id) {
            menu["AK bearbeiten"] = function() {
                window.open(event.edit_ak_url+"?_popup=1", "", "width=800,height=600,scrollbars=yes");
            };
            menu["Auf Ã„nderung hinweisen"] = function() {
                $.post("/plan/api/akmodified/", { aktermin_id: event.termin_id },
                function(data) {
                        messageBar.show("success", "Der AK wurde als verÃ¤ndert markiert. "+data.number+" Push-Benachrichtigungen wurden versandt.", 2000);
                });
            };
        }
        if (event.editable && event.avail_id) {
            menu["LÃ¶schen"] = function() {
                oplan.api.deleteRoomAvailabilityItem(event.avail_id);
            };
        }
        if (event.editable && event.termin_id) {
            menu["Aus Plan entfernen"] = function() {
                oplan.api.saveAkTerminRaw(event.termin_id, {
                    room: null,
                    start_time: null,
                    end_time: null,
                });
            };
        }
    }
    if (event.wikilink) {
        menu["Wikiseite Ã¶ffnen"] = function() {
            location = event.wikilink;
        };
    }
    return menu;
}

//==>
//==> Model code OPLAN

var oplan = {};

var STATUS = {
    'OK': 1,
    'BLOCKED': 2,
    'SHOULD_RQ': 3,
    'REQUESTED': 4,
    'SLOT': 5
};

oplan.api = {
    loadUnschedAkTermine: function() {
        var $out = $("#unsched_aktermine").html("");
        $.get("/plan/api/aktermin/?only_unscheduled=True&ordering=ak", function(aktermins) {
            aktermins.forEach(function(akt) {
                var title = akt.ak_titel;
                if(akt.ak_track != null)
                    title = "[" + akt.ak_track + "] " + title;
                $("<div class='fc-event'></div>")
                    .text(title)
                    .appendTo($out)
                    .draggable({ zIndex: 999, revert: true, })
                    .css('background', akt.ak_color)
                    .data('event', {
                        termin_id: akt.id,
                        title: title,
                        duration: akt.duration,
                        constraints_freetext: akt.ak_constraints_freetext,
                    });
            });
        });
    },

    createRoomAvailability: function(start, end, room_id) {
        if (oplan.mode == "slots") {

            var desc = prompt("Slot von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" eintragen?");
            if (desc !== null) {

                $.post("/plan/roomevents/", {
                    start: start.toISOString(),
                    end: end.toISOString(),
                    room: room_id,
                    kommentar: desc,
                    status: 5,
                }, "json")
                .success(function() {
                    $('#calendar').fullCalendar('unselect');
                    $('#calendar').fullCalendar('refetchEvents');
                })
                .error(function(data) {
                    $('#calendar').fullCalendar('unselect');
                });
                return;
            }
        } else if (oplan.mode == "availability") {
            messageBar.show("error", "Not supported...", 1000);
        } else if (oplan.mode == "aktermin") {
            var desc = prompt("Neuen AK mit Termin von "+start.format("HH:mm")+" bis "+end.format("HH:mm")+" eintragen?");
            if (desc !== null) {
                $.post("/plan/api/ak/", {
                    'titel': desc, 'beschreibung': desc, 'leiter': '?',
                }, function(ok) {
                    $.post("/plan/api/aktermin/", {
                        ak: ok.id,
                        room: room_id,
                        start_time: start.toISOString(),
                        end_time: end.toISOString(),
                        duration: (end-start)/1000, status: 4,
                        last_highlighted: moment().toISOString(),
                    }, function(ok2) {
                        $('#calendar').fullCalendar('unselect');
                        $('#calendar').fullCalendar('refetchEvents');
                    });
                });
                return;
            }
        }
        $('#calendar').fullCalendar('unselect');
    },
    onCalendarEventChange: function(event, delta, revertFunc, jsEvent, ui, view ) {
        if (oplan.mode == "slots" || oplan.mode == "availability") {
            $.post("/plan/roomevents/", {
                event_id: event.avail_id,
                start: event.start.toISOString(),
                end: event.end.toISOString(),
                room: event.resourceId,
            }, "json")
            .success(function(data) {
                $('#calendar').fullCalendar('unselect');
                $('#calendar').fullCalendar('refetchEvents');
                messageBar.show('success', ''+data.modifications+' EintrÃ¤ge verschoben', 1500);
            })
            .error(function(data) {
                revertFunc();
            });
        } else if (oplan.mode == "aktermin") {
            oplan.api.saveAkTermin(event);
        }
    },
    loadCalendarEvents: function(start, end, room_id, callback) {
        $.ajax({
            url: '/plan/roomevents/',
            dataType: 'json',
            cache: false,
            data: {
                // our hypothetical feed requires UNIX timestamps
                start: start.format('YYYY-MM-DD')+' 00:00:00',
                end: end.format('YYYY-MM-DD')+' 23:59:59',
                room: room_id,
            },
            success: function(doc) {
                var o=[];
                for(var i in doc.events) {
                    var e = doc.events[i];
                    if (e.termin_id) {
                        e.editable = (oplan.mode == "aktermin");
                        e.color = "#000000";
                        if (oplan.mode == "akreadonly") e.url = e.view_url;
                        e.borderColor=e.ak_color+" #000000 #000000 #000000";
                        e.className='bigtop';
                    } else {
                        e.editable = false; e.rendering = "background";

                        switch(e.status) {
                            case STATUS.OK:
                                e.color = "#339933";
                                if (oplan.mode == "availability") {e.rendering="";  }
                                if (oplan.mode == "availability" && !e.mgmt_id) {e.editable=true; }
                                break;
                            case STATUS.BLOCKED:
                                e.color = "#dd2222";
                                if (oplan.mode == "availability") {e.rendering="";  }
                                if (oplan.mode == "availability" && !e.mgmt_id) {e.editable=true; }
                                break;
                            case STATUS.SLOT:
                                e.color = "#113399";
                                //e.rendering="";
                                if (oplan.mode == "slots") {e.rendering=""; e.editable=true;}
                                break;
                            case STATUS.SHOULD_REQUEST:
                                e.color = "#999933";
                            case STATUS.REQUESTED:
                                e.color = "#66bb33";
                                if (oplan.mode == "availability") {e.rendering=""; }

                                break;
                        }
                    }
                    o.push(e);
                }
                callback(o);
            }
        });
    },

    saveAkTermin: function (event) {
        console.log(event.start,event.end,event.duration);
        if (!event.end) event.end = moment(event.start).add(moment.duration(event.duration));
        oplan.api.saveAkTerminRaw(event.termin_id, {
            room: event.resourceId,
            start_time: event.start.toISOString(),
            end_time: event.end.toISOString(),
            last_highlighted: moment().toISOString(),
        });
    },
    saveAkTerminRaw: function(terminId, postData) {
        $.ajax({
            url: "/plan/api/aktermin/"+terminId+"/",
            data: postData,
            method: "PATCH",
            success: function(ok) {console.log(ok);
                $('#calendar').fullCalendar('unselect');
                oplan.api.checkConflicts(terminId);
                $('#calendar').fullCalendar('refetchEvents');
                messageBar.show('success', 'Ã„nderungen am AK-Termin #'+ok.id+' '+ok.ak_titel+' wurden gespeichert', 1500);
                oplan.api.loadUnschedAkTermine();
            }
        });
    },
    checkConflicts: function(terminId) {
        messageBar.hide('warning');
        $.get("/plan/api/aktermin/"+terminId+"/check_constraints", function(result) {
            var out = [];
            if (result.constraints.fail.length > 0) {
                out.push( "Folgende EinschrÃ¤nkungen dieses Termins werden verletzt:" );
                for(var i in result.constraints.fail) {
                    var ctr = result.constraints.fail[i];
                    out.push( " - " + ctr[2] );
                }
            }
            if (result.constraints.reverse_fail.length > 0) {
                out.push( "Folgende EinschrÃ¤nkungen anderer Termine werden verletzt:" );
                for(var i in result.constraints.reverse_fail) {
                    var ctr = result.constraints.reverse_fail[i];
                    out.push( " - " + ctr[0] + " *** " + ctr[1][2] );
                }
            }
            if (out.length > 0) {
                messageBar.hide('success');
                messageBar.show("warning", out.join("<br>"), null, true);
            }
        });
    },
    deleteRoomAvailabilityItem: function(terminId) {
        $.ajax({
            url: "/plan/api/slot/"+terminId+"/",
            data: {},
            method: "DELETE",
            success: function(ok) {
                    $('#calendar').fullCalendar('unselect');
                    $('#calendar').fullCalendar('refetchEvents');
                    messageBar.show('success', 'RaumverfÃ¼gbarkeitseintrag wurde gelÃ¶scht.', 1500);
            }
        });
    },

}; //end oplan.api

//==>
//==> Django CSRF shit

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(function() {
    var languageForm = $("form[name='language-form']");
    $(":submit", languageForm).hide();
    $("select", languageForm).change(function(){languageForm.submit()});

    $("#site-name a").click(function() {
        if (!$("#header .ml").is(":visible")) {
            $("#header").addClass("expand");
            return false;
        } else if ($("#header").is(".expand")) {
            $("#header").removeClass("expand");
            return false;
        }
    })
});
