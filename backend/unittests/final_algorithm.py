# -*- coding: utf-8 -*-
import nose
from nose.tools import *
from utils import NoseUtils, SimilarityCalculator


class DummyData():
    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])

class TestMasterAlgorithm():


    @nottest
    def eq_person(self, p1, p2):
        from utils import DataValidator
        dc = DataValidator()
        dc.name = "similarity_calculator_test"
        p1 = DummyData(dc.validatePerson(p1, 0, u""))
        p2 = DummyData(dc.validatePerson(p2, 0, u""))
        return SimilarityCalculator.eq_authors(p1, p2)

    def test_persons(self):

        yield eq_, self.eq_person(u"Tomasz Witkowski", u"Tomasz Darkowski"), False
        yield eq_, self.eq_person(u"Tomasz Witkowski", u"Tomasz Matkowski"), False
        yield eq_, self.eq_person(u"Tomasz Witkowski", u"Tomasz Bąkowski"), False
        yield eq_, self.eq_person(u"Tomasz Witkowski", u"Tomasz Białkowski"), False
        yield eq_, self.eq_person(u"Stanisław Chełpa", u"Stanisław Bełza"), False
        yield eq_, self.eq_person(u"Michał Bałucki", u"Michał Zabłocki"), False
        yield eq_, self.eq_person(u"Andrzej Żurowski", u"Andrzej S. Nartowski"), False
        yield eq_, self.eq_person(u"Andrzej Żurowski", u"Andrzej Lubowski"), False
        yield eq_, self.eq_person(u"Andrzej Żbikowski", u"Andrzej Rutkowski"), False
        yield eq_, self.eq_person(u"Jean-Claude Carriere", u"Claude Farree"), False
        yield eq_, self.eq_person(u"Jan Nowicki", u"Jan Potocki"), False
        yield eq_, self.eq_person(u"Maciej Chakowski", u"Maciej Mijakowski"), False
        yield eq_, self.eq_person(u"Przemysław Ciszek", u"Jarosław Cisek"), False
        yield eq_, self.eq_person(u"Justyna Tyborowska", u"Justyna Nosorowska"), False
        yield eq_, self.eq_person(u"Jolanta Tkaczyk", u"Joanna Adamczyk"), False
        yield eq_, self.eq_person(u"Jan Wiktor Tkaczyński", u"Jolanta Tkaczyk"), False
        yield eq_, self.eq_person(u"Juliusz Verne", u"Juliusz. Tenner"), False
        yield eq_, self.eq_person(u"Roman Wieruszewski", u"Roman Warszewski"), False
        yield eq_, self.eq_person(u"Maria Paprocka", u"Maria Poprzęcka"), False
        yield eq_, self.eq_person(u"Mariola Jarocka", u"Maria Paprocka"), False
        yield eq_, self.eq_person(u"Karol May", u"Karol Marks"), False
        yield eq_, self.eq_person(u"Stefan Żeromski", u"Stefan Wroński"), False
        yield eq_, self.eq_person(u"Piotr Gryska", u"Piotr Grela"), False
        yield eq_, self.eq_person(u"Piotr Gryska", u"Piotr Baryka"), False
        yield eq_, self.eq_person(u"Michał Kolupa", u"Michał Kulesza"), False
        yield eq_, self.eq_person(u"Jacek Węsierski", u"Jacek Waniewski"), False
        yield eq_, self.eq_person(u"Jacek Węsierski", u"Jacek Siewierski"), False
        yield eq_, self.eq_person(u"Magdalena Dąbrowska", u"Halina Dąbrowska"), False
        yield eq_, self.eq_person(u"Magdalena Dąbrowska", u"Magdalena Majkowska"), False
        yield eq_, self.eq_person(u"Anna Kicińska", u"Anna Karpińska"), False
        yield eq_, self.eq_person(u"Krynia Grudzińska", u"Katarzyna Chudzińska"), False
        yield eq_, self.eq_person(u"Juliusz Słowacki", u"Euzebiusz Słowacki"), False
        yield eq_, self.eq_person(u"Magdalena Claver Pater", u"Magdalena Claver Pater"), False
        yield eq_, self.eq_person(u"Magdalena Claver Pater", u"Magdalena Bar"), False
        yield eq_, self.eq_person(u"Magdalena Claver Pater", u"Magdalena Hamer"), False
        yield eq_, self.eq_person(u"Agnieszka Frączek", u"Agnieszka Krawczyk"), False
        yield eq_, self.eq_person(u"Agnieszka Frączek", u"Agnieszka Wiącek"), False
        yield eq_, self.eq_person(u"Elżbieta Mańko", u"Elżbieta Maszke"), False
        yield eq_, self.eq_person(u"Marek Hłasko", u"Marek Zalisko"), False
        yield eq_, self.eq_person(u"Władysław Kopaliński", u"Władysław Euzebiusz Kosiński"), False
        yield eq_, self.eq_person(u"Tomasz Sielecki", u"Tomasz Stawecki"), False
        yield eq_, self.eq_person(u"Iwona Więckowska", u"Iwona Sierpowska"), False
        yield eq_, self.eq_person(u"Dorota Koziarska", u"Dorota Kozińska"), False
        yield eq_, self.eq_person(u"Paweł Marczewski", u"Paweł Zakrzewski"), False
        yield eq_, self.eq_person(u"Monika Rakusa", u"Sonia Raduńska"), False
        yield eq_, self.eq_person(u"Marek Krajewski", u"Marika Krajniewska"), False
        yield eq_, self.eq_person(u"Mariusz Czubaj", u"Dariusz Czaja"), False
        yield eq_, self.eq_person(u"Mariusz Czubaj", u"Mariusz Szuba"), False
        yield eq_, self.eq_person(u"Marta Tomaszewska", u"Marta Konarzewska"), False
        yield eq_, self.eq_person(u"Jacek Dehnel", u"Jacek Getner"), False
        yield eq_, self.eq_person(u'"Michał Rutkowski"', u"Michał Witkowski"), False
        yield eq_, self.eq_person(u"Martin Schmidt", u"Bartłomiej Schmidt"), False


        yield eq_, self.eq_person(u"Fryderyk von Schiller", u"Friedrich von Schiller"), True
        yield eq_, self.eq_person(u"Fryderyk von Schiller", u"Fryderyk Schiller"), True
        yield eq_, self.eq_person(u"Fryderyk Schiller", u"Friedrich von Schiller"), True
        yield eq_, self.eq_person(u"Aleksander Dumas", u"Alexandre Dumas"), True
        yield eq_, self.eq_person(u"Jean La Fontaine", u"Jean de La Fontaine"), True
        yield eq_, self.eq_person(u"Gustaw Flaubert", u"Gustave Flaubert"), True
        yield eq_, self.eq_person(u"Emil Zola", u"Émile Zola"), True
        yield eq_, self.eq_person(u"Aleksander Puszkin", u"Aleksandr Sergeevič Puškin"), True
        yield eq_, self.eq_person(u"Władysław Stanisław Reymont", u"Władysław Reymont"), True
        yield eq_, self.eq_person(u"Claude Farrere", u"Claude Farree"), True
        yield eq_, self.eq_person(u"Claude Farree", u"Claude Farrère"), True
        yield eq_, self.eq_person(u"Mikołaj Gogol", u"Nikolaj Vasil'evic Gogol"), True
        yield eq_, self.eq_person(u"Jerzy Żuławski", u"Jerzy. Żuławski"), True
        yield eq_, self.eq_person(u"Honore De Balzac", u"Honoriusz Balzac"), True
        yield eq_, self.eq_person(u"Honore De Balzac", u"Honore de Balzac"), True
        yield eq_, self.eq_person(u"Honore De Balzac", u"Honore de Balzac"), True
        yield eq_, self.eq_person(u"Honore De Balzac", u"Honoré de Balzac"), True
        yield eq_, self.eq_person(u"Antoni Czechow", u"Anton Czechow"), True
        yield eq_, self.eq_person(u"Juliusz Verne", u"Jules Gabriel Verne"), True
        yield eq_, self.eq_person(u"Jane Austen", u"Jane Austin"), True
        yield eq_, self.eq_person(u"Jakub Grimm", u"Jacob Grimm"), True
        yield eq_, self.eq_person(u"Joseph Bedier", u"Josheph Bedier"), True
        yield eq_, self.eq_person(u"Wiliam Makepeace Thackeray", u"William Makepeace Thackeray"), True
        yield eq_, self.eq_person(u"Fiodor Dostojewski", u"Fedor Mihajlovic Dostoevskij"), True
        yield eq_, self.eq_person(u"Magdalena Majkowska", u"Magadalena Majkowska"), True
        yield eq_, self.eq_person(u"Lewis Carroll", u"Lewis Caroll"), True
        yield eq_, self.eq_person(u"Juliusz Słowacki", u"Kuliusz Słowacki"), True
        yield eq_, self.eq_person(u"Alisa Mitchel Masiejczyk", u"Alisa Mitchel-Masiejczyk"), True
        yield eq_, self.eq_person(u"Tomasz Wasiucione", u"Tomasz Wasiucionek"), True
        yield eq_, self.eq_person(u"Tomasz Kwaśniewski", u"Tomas Kwaśniewski"), True
        yield eq_, self.eq_person(u"Dmitrij Aleksandrowicz Strelnikoff", u"Dmirij Strelnikoff"), True
        yield eq_, self.eq_person(u"Dmitrij Aleksandrowicz Strelnikoff", u"Dmitrij Strelnikoff"), True
        yield eq_, self.eq_person(u"Grzegorz Kasepke", u"Grzegorz Kasdepke"), True
        yield eq_, self.eq_person(u'"Michał Rutkowski"', u"Michał Rutkowski"), True
        yield eq_, self.eq_person(u"Małgorzata Choromańska", u"Małgorzta Chromańska"), True
        yield eq_, self.eq_person(u"Wiktor Gomulicki", u"Wiktor Teofil Gomulicki"), True
        yield eq_, self.eq_person(u"św. Katarzyna Genueńska", u"św. Katarzyna Geneueńska"), True
        yield eq_, self.eq_person(u"Ernst Theodor Amadeus Hoffmann", u"Ernst Theodor Amadeus Hoffman"), True
        yield eq_, self.eq_person(u"Adalbert von Chamisso", u"Adelbert von Chamisso"), True
        #yield eq_, self.eq_person(u"", u""), True
        #yield eq_, self.eq_person(u"", u""), True
        #yield eq_, self.eq_person(u"", u""), True
        #yield eq_, self.eq_person(u"", u""), True


        #hard
        yield eq_, self.eq_person(u"Louis Gallet", u"Louise Allen"), False
        yield eq_, self.eq_person(u"Maria Zabłocka", u"Marta Zawłocka"), False
        yield eq_, self.eq_person(u"Joseph Heller", u"Joseph Teller"), False
        yield eq_, self.eq_person(u"Michał Culepa", u"Michał Kolupa"), False
        yield eq_, self.eq_person(u"Joanna Bulska", u"Joanna Bruska"), False
        yield eq_, self.eq_person(u"Joanna Felicja Bilska", u"Joanna Bulska"), False
        yield eq_, self.eq_person(u"Magdalena Pyter", u"Magdalena Claver Pater"), False
        yield eq_, self.eq_person(u"Dorota Kozińska", u"Dorota Kozicka"), False
        yield eq_, self.eq_person(u"Piotr Sławiński", u"Piotr Skawiński"), False
        yield eq_, self.eq_person(u"Tomasz Wasiucionek", u"Tadeusz Wasiucionek"), False
        yield eq_, self.eq_person(u"Michał Koper", u"Michał Komar"), False


        yield eq_, self.eq_person(u"Charles Dickens", u"Karol Dickens"), True

