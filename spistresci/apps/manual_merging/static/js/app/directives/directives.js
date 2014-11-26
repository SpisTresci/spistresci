app.directive('book', function () {
    return {
        restrict: 'E',
        templateUrl: '/static/js/app/views/book.html',
        scope: {
            innerAlign: "@",
            obj: "="
        }
    };
});

app.directive('chooseControllers', function () {
    return {
        restrict: 'E',
        templateUrl: '/static/js/app/views/choose_controlers.html'
    };
});
