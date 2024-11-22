class Player:
    def __init__(self, name, team, position, image, nationality, goals, assists, age, league):
        self.name = name
        self.team = team
        self.position = position
        self.image = image
        self.nationality = nationality
        self.goals = goals
        self.assists = assists
        self.age = age
        self.league = league
        
    def __repr__(self):
        return (f"Player Name= {self.name},\n"
            f"team= {self.team},\n"
            f"position= {self.position},\n"
            f"goals= {self.goals},\n"
            f"assists= {self.assists},\n"
            f"age= {self.age})\n"
            f"league {self.league}\n")

    def __eq__(self, other):
        return (self.name == other.name and
                self.team == other.team and
                self.position == other.position and
                self.goals == other.goals and
                self.assists == other.assists and
                self.age == other.age and
                self.league == other.league)