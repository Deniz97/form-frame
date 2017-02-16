//getter-setters for police information, modularized for easy comminication between controllers
app.service('PoliceInfos', function () {
    var  PoliceInfo = {
        request_type: "sellform",
        police_type: "seyahat",
        infos : []
    };
    return {
        getPoliceInfo: function () {
            return PoliceInfo;
        },
        setPoliceType: function(value) {
            PoliceInfo.police_type = value;
        },
        addInfo: function(value) {
            PoliceInfo.infos.push(value);
        },
        clearInfo: function() {
            PoliceInfo.infos = [];
        },
        setRequestType: function(value) {
            PoliceInfo.request_type = value;
        }
    };
});


//wrapper to comminicate with server
app.factory('GetPoliceForms', ['$http','PoliceInfos' ,function($http,PoliceInfos) {
  return $http.post('http://localhost:8888', PoliceInfos.getPoliceInfo())
         .success(function(response) {
           return response;
         })
         .error(function(response) {
           return response;
         });
}]);






