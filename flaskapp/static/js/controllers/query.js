App.controller('queryController', ['$scope','$http','$compile', function($scope,$http,$compile) {

$scope.getQueryResults=function()
{
	$http({url:'/getQueryResults',method:"POST",params:{searchString:$scope.inputQuery}}).
		then(function successCallback(response)
		{
			console.log("Got results");
			$scope.resultCompanies=response.data['companyList']
		}
}
	
}]);
    
