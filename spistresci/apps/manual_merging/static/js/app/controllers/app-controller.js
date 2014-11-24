var book = {
    'cover': 'http://www.gandalf.com.pl/o/inferno-epub,pd,449514.jpg',
    'title': 'Inferno',
    'price_lowest': 2.43,
    'mini_books': [
        {
            'cover': 'http://ebooki.allegro.pl/imageshandler/26351/miniature/',
            'price': 0.0
        },
        {
            'cover': 'http://woblink.com/storable/pub_photos/257957-inferno.jpg',
            'price': 1.23
        }
    ]
};

app.controller('BookController', function ($scope){
    $scope.left = book;
});