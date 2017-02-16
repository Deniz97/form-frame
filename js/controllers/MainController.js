app.controller('MainController', ['$scope', '$http','PoliceInfos', function($scope,$http,PoliceInfos) {
  
	$scope.message= "Police Tipini Giriniz";
	$scope.policeType = ""


	$scope.FetchSellForm = function( ) {	
		PoliceInfos.setRequestType("sellform") 
		PoliceInfos.setPoliceType( $scope.policeType);
		window.location.href = '#/SellForm'
	};

	
  
  
}]);


app.controller('SellFormCtrl', ['$scope', 'GetPoliceForms','PoliceInfos',function($scope,GetPoliceForms,PoliceInfos) {
  

	$scope.policeType = PoliceInfos.getPoliceInfo().police_type
	$scope.messagee= $scope.policeType + " Policesi";
	$scope.dummy_infos = [];
	
	GetPoliceForms.success( function(response) {
           			response=response+""
           			
	
			$scope.SellFormArray = response.split(",");
	
           			
           			console.log($scope.SellFormArray)

           			for (var i = 0; i  < $scope.SellFormArray.length ; i++) {
           				
           				$scope.dummy_infos.push("filler");
           			};
	}).error( function(err,status) {
			$scope.err = { message: err, stat: status};
        			console.log($scope.err.stat); 
        			console.log($scope.err); 
        			console.log($scope.err.message); 
			$scope.SellFormArray = "still empty";
			$scope.dummy_infos.push("filler");

	});




	$scope.FetchPoliceForm = function () {
		PoliceInfos.clearInfo()
		PoliceInfos.setRequestType("policeoffer")
		console.log($scope.dummy_infos)
		for (var i = 0; i  < $scope.dummy_infos.length ; i++) {;
           			PoliceInfos.addInfo( $scope.dummy_infos[i] )
           		};
           		console.log(PoliceInfos.getPoliceInfo())
           		window.location.href = '#/PoliceForm'
		
	}
}]);

app.controller('PoliceFormCtrl', ['$scope', 'GetPoliceForms','PoliceInfos', function($scope,GetPoliceForms,PoliceInfos) {
  
	$scope.messageee= "POLICE FORM"
	
	const socket = new WebSocket('ws://localhost:8899');

	// Connection opened
	socket.addEventListener('open', function (event) {
	    socket.send( JSON.stringify( PoliceInfos.getPoliceInfo() ) );
	    console.log("Send" + JSON.stringify( PoliceInfos.getPoliceInfo() ) )
	});

	// Listen for messages
	socket.addEventListener('message', function (event) {
	    console.log('Message from server', event.data);
	});


  
}]);