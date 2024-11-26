# NFL Import
from espn_api.football import League
import pandas as pd
import math

class FFBookie(object):
    def __init__(self):
        self.league = self._setLeague(605278, 2024)
        self.odds_df = pd.DataFrame(columns=["matchup", "home", "away", "spread (+110)", "O/U (+110)", "ML"])
        
    def __repr__(self) -> str:
        return "Odds for Domination League"

    def _setLeague(self, league_id: int, year: int) -> League:
        swid = "{DE08842B-7384-4C68-B7C5-AB3BB102E995}"
        espn_s2 = "AEBDU030JkQcU9Pa5FCCQczqZoZIGjrRqt63%2BY8iYA3Eb2CE4KbLx0xdfwG2EFFJPA%2FrpUSGfuOVRfCCeX%2F%2BYX%2BBmJ6gFvTvE7UMZpSgH0WBgT%2BZMWYVWC6cJARuctk5ck5uToViuedkNwdMX55Qbx9uaMfknXGUsd5YtNXpeDnzYeVEj6x3Hrrfhi0E8LJCkBVBulS3LssLdUc2Bh057ZnVIVNqHN25DLcGnGtvCZE7js8lug0cj7qoTklTMJKvvn6w9WE1iWg0gKod40RpuorelZBhPXagJfz3n5h088%2BkjqHRIzbAdsurOux00ys3V1c%3D"
        return League(league_id=league_id, year=year, espn_s2=espn_s2, swid=swid)

    def _getSpread(self, home_proj: float, away_proj: float) -> str:
        diff = round((home_proj - away_proj), 2)
        return f"-{diff}" if diff > 0 else f"+{-1 * diff}"

    def _getOU(self, home_proj: float, away_proj: float) -> str:
        tot = round((home_proj + away_proj), 1)
        return f"{tot}"

    def _getML(self, home_proj: float, away_proj: float, k=0.05, vig=0.048) -> str:
        # Calculate the spread
        spread = home_proj - away_proj

        # Convert spread to win probabilities using a logistic function
        home_win_prob = 1 / (1 + math.exp(-k * spread))
        away_win_prob = 1 - home_win_prob

        # Adjust probabilities to include vig
        total_prob = home_win_prob + away_win_prob
        home_win_prob_adjusted = home_win_prob / total_prob * (1 - vig)
        away_win_prob_adjusted = away_win_prob / total_prob * (1 - vig)

        # print(f"{home_win_prob_adjusted}, {away_win_prob_adjusted}")

        # Convert probabilities to money lines
        def prob_to_money_line(prob):
            if prob > 0.5:  # Favorite
                return round(-100 / (abs(prob - 1)))
            else:  # Underdog
                return round((1 / prob - 1) * 100)

        home_money_line = prob_to_money_line(home_win_prob_adjusted)
        away_money_line = prob_to_money_line(away_win_prob_adjusted)

        if home_money_line > 0 and away_money_line > 0:
            home_money_line *= -1
            away_money_line *= -1
        
        if home_money_line > 0:
            return f"home ML: +{home_money_line}, away ML: {away_money_line}"
        elif away_money_line > 0:
            return f"home ML: {home_money_line}, away ML: +{away_money_line}"
        else:
            return f"home ML: {home_money_line}, away ML: {away_money_line}"

    def calculate_odds(self, week: int) -> None:
        box_scores = self.league.box_scores(week)

        for matchup in range(len(box_scores)):
            home_team = box_scores[matchup].home_team
            away_team = box_scores[matchup].away_team

            home_proj = box_scores[matchup].home_projected
            away_proj = box_scores[matchup].away_projected

            spread = self._getSpread(home_proj, away_proj)
            ou = self._getOU(home_proj, away_proj)
            ml = self._getML(home_proj, away_proj)

            new_row = {"matchup": matchup + 1, "home": home_team.team_name, "away": away_team.team_name, "spread (+110)": spread, "O/U (+110)": ou, "ML": ml}
            self.odds_df = pd.concat([self.odds_df, pd.DataFrame([new_row])], ignore_index=True)

    def save_odds(self, week) -> None:  
        self.odds_df.to_csv(f"week{week}book.csv", index=False)

if __name__ == "__main__":
    bookie = FFBookie()

    week = 13
    bookie.calculate_odds(week)
    bookie.save_odds(week)
