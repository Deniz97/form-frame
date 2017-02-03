//Not used yet, currently http services are done in controllers
app.factory('GetPoliceForms', ['$http', function($http) {
  return $http.post('http://127.0.0.1:8888', "TODO:FIX HERE")
         .success(function(data) {
           return data;
         })
         .error(function(data) {
           return data;
         });
}]);

//getter-setters for police information, modularized for easy comminication between controllers
app.service('PoliceInfos', function () {
    var  PoliceInfo = {
        PoliceType: "araba",
        infos : []
    };
    return {
        getPoliceInfo: function () {
            return PoliceInfo;
        },
        setPoliceType: function(value) {
            PoliceInfo.PoliceType = value;
        },
        addInfo: function(value) {
            PoliceInfo.infos.push(value);
        }
    };
});


