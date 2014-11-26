
app.controller('BooksController', ['$scope', '$http', '$q', function ($scope, $http, $q){
    $scope.books = [];

    $http.get('/api/similar-minibooks/1/?format=json').success(function(data){
        var similar_pair = data;

        var book = {
            left: null,
            right: null,
            status: null
        };

        var left_promise = $http.get(similar_pair.lower_masterbook).success(function(data){
                book.left = data;
            });


        var right_promise = $http.get(similar_pair.higher_masterbook).success(function(data){
                book.right = data;
            });


        $q.all([left_promise, right_promise]).then(function(data){
            $scope.books.push(book);
        });

    });

    $scope.selected_pair = 0;

    $scope.selectPair = function(pairNum){
        $scope.selected_pair = pairNum;

    };

    $scope.isSelected = function(checkPair){
        return $scope.selected_pair == checkPair;
    };

    $scope.approve = function(pairNum){
        $scope.books[pairNum].status = 'approved';
    };

    $scope.isApproved = function(pairNum){
        return $scope.books[pairNum].status == 'approved';
    };

    $scope.reject = function(pairNum){
        $scope.books[pairNum].status = 'rejected';
    };

    $scope.isRejected = function(pairNum){
        return $scope.books[pairNum].status == 'rejected';
    };

    $scope.leave_undecided = function(pairNum){
        $scope.books[pairNum].status = 'undecided';
    };

    $scope.isUndecided = function(pairNum){
        return $scope.books[pairNum].status == 'undecided';
    };


}]);