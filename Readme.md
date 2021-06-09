SpisTresci.pl
=================

SpisTresci.pl to wyszukiwarka i porównywarka ebooków, audiobooków i książek tradycyjnych. 

Wymagania Systemowe
-------------------
- system linux (przetestowane na: Ubuntu 12.04/14.04, Debian 6/7)


Pobieranie źródeł
----------


    mkdir ~/devel
    git clone git@dev.spistresci.pl:/var/git/spistresci_frontend.git spistresci


Pakiety sytemowe
----------

Spis potrzebnych pakietów systemowych znajduje się w pliku `requirements.apt`. Instalację można wywołać poprzez:

    cd ~/devel/spistresci/
    sudo apt-get -y install $(grep -vE "^\s*#" requirements.apt  | tr "\n" " ")


Tworzenie Wirtualnego Środowiska
--------------------------------

Najpierw należy wyedytować plik `~/.bashrc` dodając **na jego końcu** poniższe 3 linijki:


    export WORKON_HOME=$HOME/.virtualenvs
    export PROJECT_HOME=$HOME/devel
    source /usr/local/bin/virtualenvwrapper.sh

Po zapisaniu pliku, by zmiany od razu wczytać, należy wykonać:

    source ~/.bashrc


By w przyszłości korzystając z polecenia workon od razu przechodzić do katalogu projektu, należy wyedytować plik ~/.virtualenvs/postactivate dodając do niego:

    PROJECT_NAME=$(echo $VIRTUAL_ENV|awk -F'/' '{print $NF}')
    cd $PROJECT_HOME/$PROJECT_NAME

następnie w końcu wykonujemy polecenie:

    mkproject spistresci

Pakiety Pythonowe
-----------------

    workon spistresci
    pip install -r requirements.pip
    
    
Pierwsza konfiguracja
---------------------

    ./manage.py syncdb
    sass --update spistresci/static/scss/:spistresci/static/css/
    
Ściągnięcie i konfiguracja lokalnej wersji Solr'a    

    ./manage.py downloadsolr
    ./manage.py configuresolr
    

Uruchomienie
------------

    ./manage.py runserver
    
