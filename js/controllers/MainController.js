app.controller('MainController', ['$scope', '$http','PoliceInfos', function($scope,$http,PoliceInfos) {
  
	$scope.message= "Police Tipini Giriniz";
	$scope.policeType = ""


	$scope.FetchSellForm = function( ) {	
		PoliceInfos.setPoliceType($scope.policeType);
		window.location.href = '#/SellForm'
	};

	
  
  
}]);


app.controller('SellFormCtrl', ['$scope', '$http','PoliceInfos', function($scope,$http,PoliceInfos) {
  
	
	$scope.policeType = PoliceInfos.getPoliceInfo().PoliceType
	$scope.messagee= $scope.policeType + " Policesi";
	$scope.dummy_infos = [];


	$http.post('http://127.0.0.1:8888', $scope.policeType)
         		.then(function(data) {
           			//TO DO: TURN DATA INTO ARRAY
           			$scope.SellFormArray = data;
           			for (var i = 0; i  < data.length ; i++) {
           				
           				$scope.dummy_infos.push("filler");
           			};
         		},
         		function(err,status) {
			$scope.err = { message: err, stat: status};
        			console.log($scope.err.stat); 
        			console.log($scope.err.message); 
			$scope.SellFormArray = "still empty";
			$scope.dummy_infos.push("filler");
         		});

	$scope.FetchPoliceForm = function () {
		//update the actual police-infos-array
		//TODO: clear the actual array first, just in case
		for (var i = 0; i  < dummy_infos.length ; i++) {;
           			PoliceInfos.addInfo( dummy_infos[i] )
           		};
           		window.location.href = '#/PoliceForm'
		
	}
}]);

app.controller('PoliceFormCtrl', ['$scope', '$http','PoliceInfos', function($scope,$http,PoliceInfos) {
  
	$scope.message= "Police Tipini Giriniz";
	$scope.policeType = ""


	$scope.FetchSellForm = function( ) {	
		PoliceInfos.setPoliceType($scope.policeType);
		window.location.href = '#/SellForm'
	};

	
  
  
}]);