"""
given teams.json, generate a bracket for the tournament,
The list of teams is sorted by fist round match-ups (element 0 plays element 1, element 2 plays element 3, etc.)
and grouped by region (i.e the first 16 teams are from the East, the next 16 are from the West, etc.)
create a bracket that shows the match-ups for each round of the tournament
"""
import argparse
import json
import random
import pandas as pd


class EloRatingSystem:
    def __init__(self, k_factor=20, home_advantage=100, teams=None):
        self.k_factor = k_factor
        self.home_advantage = home_advantage
        if teams is None:
            self._teams = {}
        else:
            self._teams = teams

    @property
    def teams(self):
        return self._teams

    @classmethod
    def from_list(cls, team_list: list[dict], k_factor=20, home_advantage=100):
        team_ratings = {team['name']: team['elo'] for team in team_list}
        return cls(k_factor, home_advantage, team_ratings)

    @staticmethod
    def _static_predict_outcome(rating1: float, rating2: float, home_advantage):
        rating1 += home_advantage
        expected_outcome1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
        return expected_outcome1

    def _predict_outcome(self, rating1: float, rating2: float):
        return self.__class__._static_predict_outcome(rating1, rating2, home_advantage=self.home_advantage)

    def predict_outcome(self, team1: str, team2: str):
        rating1 = self._teams.get(team1, None)
        rating2 = self._teams.get(team2, None)
        return self._predict_outcome(rating1, rating2)

    def update_ratings(self, team1: str, team2: str, outcome):
        rating1 = self._teams.get(team1, None)
        rating2 = self._teams.get(team2, None)
        expected_outcome1 = self._predict_outcome(rating1, rating2)
        if outcome == 1:
            actual_outcome1 = 1
        elif outcome == 0 :
            actual_outcome1 = 0.5
        else:
            actual_outcome1 = 0
        rating1 += self.k_factor * (actual_outcome1 - expected_outcome1)
        rating2 += self.k_factor * ((1 - actual_outcome1) - (1 - expected_outcome1))
        self._teams[team1] = rating1
        self._teams[team2] = rating2


def generate_bracket(teams, groups=1):
    # make equal groups of teams
    group_size = len(teams) // groups
    # split teams into groups
    groups = [teams[i:i+group_size] for i in range(0, len(teams), group_size)]

    grouped_matchups = []
    for group in groups:
        # make match-ups
        match_ups = [group[i:i+2] for i in range(0, len(group), 2)]
        grouped_matchups.append(match_ups)

    return grouped_matchups


def simulate_tournament_round(teams: list[str], elo_system: EloRatingSystem):
    """
    Simulate a round of the tournament,
    Note: this function modifies the state of the elo_system by updating
    the ratings of the teams who played in the round

    :param teams: the teams playing in the round
    :param elo_system: the elo rating system for predicting outcomes
    :return: the teams that will advance to the next round
    """
    next_round = []
    for i in range(0, len(teams), 2):
        team1 = teams[i]
        team2 = teams[i+1]
        expected_outcome = elo_system.predict_outcome(team1, team2)
        random_number = random.random()
        if random_number <= expected_outcome:
            outcome = 1
            next_round.append(team1)
        else:
            outcome = 0
            next_round.append(team2)
        elo_system.update_ratings(team1, team2, outcome)

    return next_round


def simulate_tournament(teams: list[str], elo_system):
    """
    Simulate the entire tournament, simulating each round until a winner is determined
    :param teams:
    :param elo_system:
    :return: a log of each round until a winner is determined
    """
    rounds = [teams]
    rounds_and_ratings = [[(team, elo_system.teams[team]) for team in teams]]
    while len(teams) > 1:
        teams = simulate_tournament_round(teams, elo_system)
        rounds.append(teams)
        rounds_and_ratings.append([(team, elo_system.teams[team]) for team in teams])
    return rounds_and_ratings


def main():
    parser = argparse.ArgumentParser(description="Process JSON input and output CSV file.")
    parser.add_argument('--input', required=True, help="Path to the input JSON file.")
    parser.add_argument('--output', required=True, help="Path to the output CSV file.")
    args = parser.parse_args()
    with open(args.input) as f:
        _teams_data = json.load(f)['teams']

    _elo_system = EloRatingSystem.from_list(_teams_data, home_advantage=0)
    _teams = [team['name'] for team in _teams_data]
    _res = simulate_tournament(_teams, _elo_system)
    # with result, create a dataframe by iterating result backwards, creating a dataframe from each matchup_round and adding a matchup_round column equal to the iteration number
    _df = pd.DataFrame()
    for i, tourney_round in enumerate(_res[::-1]):
        _df = pd.concat([_df, pd.DataFrame(tourney_round, columns=['team', 'rating']).assign(round=i)], ignore_index=True)

    _df.to_csv(args.output)


if __name__ == '__main__':
    main()







