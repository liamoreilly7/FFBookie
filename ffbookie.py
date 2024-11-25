# NFL Import
from espn_api.football import League
import pandas as pd

class FFBookie(object):
    def __init__(self):
        self.league = self._setLeague(605278, 2024)
        self.odds_df = pd.DataFrame(columns=["home", "away", "spread", "O/U", "Odds"])
        
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

    def calculate_odds(self, week: int) -> None:
        box_scores = self.league.box_scores(week)

        for matchup in range(len(box_scores)):
            home_team = box_scores[matchup].home_team
            away_team = box_scores[matchup].away_team

            home_proj = box_scores[matchup].home_projected
            away_proj = box_scores[matchup].away_projected

            spread = self._getSpread(home_proj, away_proj)
            ou = self._getOU(home_proj, away_proj)

            new_row = {"home": home_team, "away": away_team, "spread": spread, "O/U": ou, "Odds": "+110"}
            self.odds_df = pd.concat([self.odds_df, pd.DataFrame([new_row])], ignore_index=True)

    def save_odds(self, week) -> None:  
        self.odds_df.to_csv(f"week{week}book.csv", index=False)

if __name__ == "__main__":
    bookie = FFBookie()

    week = 12
    bookie.calculate_odds(week)
    bookie.save_odds(week)
