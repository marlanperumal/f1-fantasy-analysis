# F1 Fantasy Analysis

A comprehensive application for analyzing Formula 1 fantasy data, providing insights through a REST API and a modern web interface.

This repo contains code and data to analyse the F1 Fantasy game on the [F1 website](https://fantasy.formula1.com/en/). The 
game allows selection of a team consisting of 2 constructors and 5 drivers, who will score points at each F1 race through the 
year. There is a spend cap of $100,000,000 that can be used to pay for the drivers and constructors, whose price will 
fluctuate throughout the year as their fortunes wax and wane.

- An overview of the rules are found [here](https://fantasy.formula1.com/en/how-to-play)
- Full rules include scoring are [here](https://fantasy.formula1.com/en/game-rules)
- The current driver and constructor lineup and prices are [here](https://fantasy.formula1.com/en/statistics/details?
tab=driver)

The objective will be to use the contents of the repo to select the best team and continuously manage transfers throughout the 
season.

## Analysis Plan

- [x] Setup Scoring Rules
- [ ] Develop driver position model
- [x] Setup Driver Data
- [ ] Allow for Team selection
- [ ] Simulate Race
- [ ] Optimise team
- [ ] Get historic data
- [ ] Simulate Previous Seasons
- [ ] Setup Frontend

## Project Structure

```
f1-fantasy-analysis/
├── backend/                # Backend source code
│   ├── api/                # API endpoints and server
│   ├── analysis/           # Analysis algorithms
│   ├── data/               # Data models and fetchers
│   └── utils/              # Utility functions
├── webapp/                 # Frontend web application
│   ├── src/                # Frontend source code
│   │   ├── app/            # Next.js app router pages
│   │   │   ├── drivers/     # Drivers analysis page
│   │   │   ├── teams/       # Teams analysis page
│   │   │   ├── analysis/    # Advanced analysis tools
│   │   │   └── simulator/   # Race simulator
│   │   ├── components/     # React components
│   │   └── lib/            # Frontend utilities
│   └── public/             # Static assets
├── tests/                  # Test files
├── data/                   # Data storage (created at runtime)
├── pyproject.toml          # Backend project configuration
├── package.json            # Frontend project configuration
└── README.md               # Project documentation
```

## Features

### Data Analysis
- Fetch current F1 season data (races, drivers, teams)
- Calculate value efficiency for drivers and teams
- Analyze form trends
- Recommend optimal team selections based on budget constraints
- Advanced data analysis using Polars for high-performance processing

### User Interface
- Dashboard with key metrics and insights
- Driver and team analysis with value metrics
- Advanced analysis tools for optimizing team selection
- Race simulator for predicting fantasy points
- Interactive UI for building and testing fantasy teams

## Requirements

- Python 3.13+ (for backend)
- Node.js 18.17+ (for frontend)
- uv (Python package manager)
- pnpm 8.0+ (Node.js package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/f1-fantasy-analysis.git
cd f1-fantasy-analysis
```

2. Set up the backend:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add --dev hatchling
uv add fastapi uvicorn polars numpy matplotlib seaborn requests python-dotenv pydantic httpx pytest
```

3. Set up the frontend:

```bash
pnpm install
```

4. Configure environment variables:

Create a `.env.local` file in the root directory with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage

### Running the Application

Start the backend API server:

```bash
uv run backend/main.py
```

Start the frontend development server:

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

### Building for Production

Build the frontend for production:

```bash
pnpm build
pnpm start
```

## API Endpoints

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/races` - Get current season races
- `GET /api/v1/drivers` - Get drivers with fantasy data
- `GET /api/v1/teams` - Get teams with fantasy data
- `GET /api/v1/analysis/driver-value` - Get driver value analysis
- `GET /api/v1/analysis/team-value` - Get team value analysis
- `GET /api/v1/analysis/form-trends` - Get driver form trends
- `GET /api/v1/analysis/optimal-team` - Get optimal team selection
- `GET /api/v1/analysis/team-performance` - Get team performance metrics
- `GET /api/v1/analysis/price-points-correlation` - Get correlation between price and points
- `GET /api/v1/analysis/undervalued-drivers` - Find undervalued drivers
- `GET /api/v1/analysis/predict-points` - Predict future points based on current performance
- `GET /api/v1/analysis/optimal-team-advanced` - Advanced team selection with team constraints

## Testing

Run tests using pytest:

```bash
uv run -m pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [Ergast F1 API](https://ergast.com/mrd/) for providing F1 data
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework
- [Polars](https://pola.rs/) for high-performance data processing
- [Next.js](https://nextjs.org/) for the frontend framework
- [TanStack Query](https://tanstack.com/query) for data fetching
- [Tailwind CSS](https://tailwindcss.com/) for styling