"""Data fetcher module for retrieving F1 data from external sources."""

import json
import logging
from typing import Dict, List, Optional, Union

import httpx
from pydantic import ValidationError

from src.data.models import Driver, Race, Team

logger = logging.getLogger(__name__)


class F1DataFetcher:
    """Class for fetching F1 data from external sources."""

    def __init__(self, base_url: str = "https://ergast.com/api/f1"):
        """Initialize the F1DataFetcher.

        Args:
            base_url: Base URL for the Ergast F1 API
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()

    async def get_current_season_races(self) -> List[Race]:
        """Get the current season's race schedule.

        Returns:
            List of Race objects
        """
        url = f"{self.base_url}/current.json"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            races = []
            for race_data in data["MRData"]["RaceTable"]["Races"]:
                race = Race(
                    id=int(race_data["round"]),
                    name=race_data["raceName"],
                    circuit=race_data["Circuit"]["circuitName"],
                    date=f"{race_data['date']}T{race_data.get('time', '00:00:00Z')}",
                    country=race_data["Circuit"]["Location"]["country"],
                    completed=False,  # This would need to be determined based on current date
                )
                races.append(race)
            return races
        except (httpx.HTTPError, KeyError, ValidationError) as e:
            logger.error(f"Error fetching race schedule: {e}")
            return []

    # Note: The Ergast API doesn't provide fantasy pricing data
    # In a real application, you would need to fetch this from the official F1 Fantasy API
    # This is a placeholder implementation
    async def get_drivers(self) -> List[Driver]:
        """Get the current drivers with mock fantasy data.

        Returns:
            List of Driver objects with mock fantasy data
        """
        url = f"{self.base_url}/current/drivers.json"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            drivers = []
            for idx, driver_data in enumerate(data["MRData"]["DriverTable"]["Drivers"]):
                # Mock fantasy data
                driver = Driver(
                    id=idx + 1,
                    name=f"{driver_data['givenName']} {driver_data['familyName']}",
                    team="Unknown",  # The Ergast API doesn't include team info in this endpoint
                    price=float(f"{(idx % 5) + 10}.{(idx % 10) * 5}"),  # Mock price
                    points=float(idx * 10),  # Mock points
                    form=float(idx % 5),  # Mock form
                )
                drivers.append(driver)
            return drivers
        except (httpx.HTTPError, KeyError, ValidationError) as e:
            logger.error(f"Error fetching drivers: {e}")
            return []

    # Similarly, this is a placeholder for team data
    async def get_teams(self) -> List[Team]:
        """Get the current teams with mock fantasy data.

        Returns:
            List of Team objects with mock fantasy data
        """
        url = f"{self.base_url}/current/constructors.json"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            data = response.json()
            
            teams = []
            for idx, team_data in enumerate(data["MRData"]["ConstructorTable"]["Constructors"]):
                # Mock fantasy data
                team = Team(
                    id=idx + 1,
                    name=team_data["name"],
                    price=float(f"{(idx % 3) + 20}.{idx * 5}"),  # Mock price
                    points=float(idx * 15),  # Mock points
                    form=float((idx % 5) + 1),  # Mock form
                )
                teams.append(team)
            return teams
        except (httpx.HTTPError, KeyError, ValidationError) as e:
            logger.error(f"Error fetching teams: {e}")
            return [] 