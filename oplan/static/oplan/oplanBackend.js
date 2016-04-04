angular.module("oplanBackend", [])


.factory('oplanHttp', function($http, $rootScope) {
    return {
        doGet: function(apiName, params) {
            return $http.get('/api/v1/' + $rootScope.vk + '/' + apiName + "?" + (params ? $.param(params) : ''));
        },
        
        doPost: function(apiName, urlParams, data, method) {
            return $http({
                method: method || 'POST',
                url: '/api/v1/' + $rootScope.vk + '/' + apiName + "?" + $.param(urlParams),
                data: $.param(data),
                headers: {'Content-Type': 'application/x-www-form-urlencoded'}
            })
        },
        
        doPUT: function(url, urlParams, data) {
            return this.doPost(url, urlParams, data, "PUT");
        },
        doDELETE: function(url, urlParams, data) {
            return this.doPost(url, urlParams, data, "DELETE");
        },
        
        belegeRaum: function(terminId, belegungId, nummer) {
            return this.doPUT("belegung/"+belegungId, {},
              {apply: nummer});
        },
        
        updateBelegung: function(terminId, belegungId, data) {
            return this.doPUT("ak/"+terminId+"/raumbedarf/"+belegungId,  {},
              data);
        },
        createBelegung: function(terminId, komm, min_platz) {
            return this.doPost("ak/"+terminId+"/raumbedarf",  {},
              { ak_id: terminId, kommentar: komm, min_platz: min_platz });
        },
        deleteBelegung: function(terminId, belegungId) {
            return this.doDELETE("ak/"+terminId+"/raumbedarf/"+belegungId,  {},
              {});
        },
        
        moveTermin: function(terminId, start, end, moveAll) {
            return this.doPUT("ak/"+terminId, {}, {
                von: start.format ? start.format("YYYY-MM-DD HH:mm:ss") : start, 
                bis: end.format ? end.format("YYYY-MM-DD HH:mm:ss") : end, 
                all: moveAll ? "true" : ""
            });
        },
        
        newTermin: function(start, end, desc, gruppe) {
            return this.doPost('ak', {}, { 
                create_von: start.format ? start.format("YYYY-MM-DD HH:mm:ss") : start, 
                create_bis: end.format ? end.format("YYYY-MM-DD HH:mm:ss") : end,
                kurztitel: desc,
                zielgruppe: gruppe
            });
        },
        
        deleteRaumFrei : function(id) {
          return this.doDELETE("raumbuchung/" + id, {}, {"delete": "yes", "id": id});
        },
        
        setRaumFrei: function(id, nummer, von, bis, kom, status) {
            if (!von.format) von=moment(von);
            if (!bis.format) bis=moment(bis);
            var data = {
              raum_nummer:nummer,von:von.format("YYYY-MM-DD HH:mm:ss"), bis: bis.format("YYYY-MM-DD HH:mm:ss"),
              kommentar: kom, status: status
            };
            if (id) data.id = id;
            return this.doPost("/api/v1/raumbuchung", {}, data);
        },
        
        listStundenplans: function() {
            return this.doGet("zielgruppen", {});
        },
        listVeranstaltungen: function() {
            return $http.get('/api/v1/veranstaltungen');
        },
      
    };
})


;