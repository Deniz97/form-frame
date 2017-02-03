var app = angular.module('myApp', ['ngRoute']);


app.config(function ($routeProvider) { 
  $routeProvider 
    .when('/', { 
      controller: 'MainController', 
      templateUrl: 'views/BasicForm.html' 
    }) 
    .when('/SellForm', {
      controller:'SellFormCtrl',
      templateUrl: 'views/SellForm.html'
    })
    .when('/PoliceForm', {
      controller:'PoliceFormCtrl',
      templateUrl: 'views/PoliceForm.html'
    })

    .otherwise({ 
      redirectTo: '/' 
    }); 
});
