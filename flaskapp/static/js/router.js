App.config(function($routeProvider) {
  $routeProvider
	.when('/', {
	templateUrl: 'static/views/query.html',
	controller: 'queryController'
	})
	.when('/query', {
	templateUrl: 'static/views/query.html',
	controller: 'queryController'
	})
	.when('/train', {
	templateUrl: 'static/views/train.html',
	controller: 'trainController'
	})
	.when('/userprofile', {
	templateUrl: 'static/views/userprofile.html',
	controller: 'uerProfileController'
	})
    .otherwise({
      redirectTo: '/404'
    });
});
