import requests


class Superhero:
    __url = 'https://superheroapi.com/api/2619421814940190/search/'
    __all_stats = {}

    def __init__(self, name):
        self.__name = name
        self.__information = None
        try:
            Superhero.__all_stats[self.name] = {'id': self.id, 'intelligence': self.intelligence}
        except KeyError:
            raise KeyError(f'The character {self.name} does not exist on the website')

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        del Superhero.__all_stats[self.name]
        self.__name = new_name
        self.__information = None
        Superhero.__all_stats[self.name] = {'id': self.id, 'intelligence': self.intelligence}


    @property
    def information(self):
        """
        Request all information about the superhero from the server
        """
        if self.__information is None:
            self.__information = requests.get(Superhero.__url + self.name).json()
        return self.__information

    @property
    def id(self):
        return self.information['results'][0]['id']

    @property
    def intelligence(self):
        return self.information['results'][0]['powerstats']['intelligence']

    @classmethod
    def superheroes_stats(cls):
        return cls.__all_stats

    def __lt__(self, other):
        return self.intelligence < other.intelligence

    def __repr__(self):
        return f'Superhero - {self.name}, Intelligence - {self.intelligence}'


if __name__ == '__main__':
    first = Superhero('Hulk')
    second = Superhero('Captain America')
    third = Superhero('Thanos')

    print(Superhero.superheroes_stats())
    print(f'Minimal intelligence - {min(Superhero.superheroes_stats())}')

    third.name = 'Sage'

    print(Superhero.superheroes_stats())
