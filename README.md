# F1 Fantasy Analysis

A Python application for analyzing Formula 1 fantasy data and providing insights through a REST API.

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

- [] Setup Scoring Rules
- [] Develop driver position model
- [] Setup Driver Data
- [] Allow for Team selection
- [] Simulate Race
- [] Optimise team
- [] Get historic data
- [] Simulate Previous Seasons
- [] Setup Frontend

## Features

- Fetch current F1 season data (races, drivers, teams)
- Calculate value efficiency for drivers and teams
- Analyze form trends
- Recommend optimal team selections based on budget constraints
- Advanced data analysis using Polars for high-performance processing
- RESTful API for accessing all analysis features

## Project Structure

```
f1-fantasy-analysis/
├── src/                    # Source code
│   ├── api/                # API endpoints and server
│   ├── analysis/           # Analysis algorithms
│   ├── data/               # Data models and fetchers
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── data/                   # Data storage (created at runtime)
├── pyproject.toml          # Project configuration
└── README.md               # Project documentation
```

## Requirements

- Python 3.13+
- uv (Python package manager)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/f1-fantasy-analysis.git
cd f1-fantasy-analysis
```

2. Create a virtual environment and install dependencies using uv:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add --dev hatchling
uv add fastapi uvicorn polars numpy matplotlib seaborn requests python-dotenv pydantic httpx pytest
```

## Configuration

The application can be configured using environment variables or a `.env` file in the project root:

```
# API configuration
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=False

# External API configuration
ERGAST_API_URL=https://ergast.com/api/f1

# Fantasy settings
DEFAULT_BUDGET=100.0
MAX_DRIVERS=5

# Cache settings
CACHE_ENABLED=True
CACHE_TTL=3600
```

## Usage

### Running the API Server

```bash
uv run src/main.py
```

Or with custom parameters:

```bash
uv run src/main.py --host 127.0.0.1 --port 8080 --debug --log-level DEBUG
```

### API Endpoints

#### Basic Endpoints
- `GET /` - API information
- `GET /health` - Health check
- `GET /api/v1/races` - Get current season races
- `GET /api/v1/drivers` - Get drivers with fantasy data
- `GET /api/v1/teams` - Get teams with fantasy data

#### Analysis Endpoints
- `GET /api/v1/analysis/driver-value` - Get driver value analysis
- `GET /api/v1/analysis/team-value` - Get team value analysis
- `GET /api/v1/analysis/form-trends` - Get driver form trends
- `GET /api/v1/analysis/optimal-team` - Get optimal team selection

#### Advanced Analysis Endpoints (Polars-based)
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

# F1 Fantasy Analysis Web Application

A modern web application for analyzing Formula 1 fantasy data and optimizing team selection.

## Features

- Dashboard with key metrics and insights
- Driver and team analysis with value metrics
- Advanced analysis tools for optimizing team selection
- Race simulator for predicting fantasy points
- Interactive UI for building and testing fantasy teams

## Tech Stack

- **Framework**: Next.js 15 with React 19 and App Router
- **Styling**: Tailwind CSS with shadcn/ui components
- **State Management**: Zustand
- **API Integration**: TanStack Query
- **Drag and Drop**: dnd-kit (for team builder)
- **Package Manager**: pnpm

## Prerequisites

- Node.js 18.17 or later
- pnpm 8.0 or later
- Backend API running (see main project README)

## Getting Started

1. Install dependencies:

```bash
pnpm install
```

2. Set up environment variables:

Create a `.env.local` file in the root directory with the following variables:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. Run the development server:

```bash
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser to see the application.

## Project Structure

```
f1-fantasy-analysis/
├── public/                  # Static assets
├── src/
│   ├── app/                 # App router pages
│   │   ├── (dashboard)/     # Dashboard layout and pages
│   │   │   ├── drivers/     # Drivers analysis page
│   │   │   ├── teams/       # Teams analysis page
│   │   │   ├── analysis/    # Advanced analysis tools
│   │   │   └── simulator/   # Race simulator
│   │   ├── api/             # API routes
│   │   ├── layout.tsx       # Root layout
│   │   └── page.tsx         # Home page
│   ├── components/          # Reusable components
│   │   └── ui/              # UI components from shadcn
│   └── lib/                 # Utility functions and hooks
│       ├── api/             # API client
│       └── utils/           # Helper functions
├── .env.local               # Environment variables
├── next.config.ts           # Next.js configuration
├── package.json             # Project dependencies
└── tailwind.config.js       # Tailwind CSS configuration
```

## Connecting to the Backend

The web application connects to the F1 Fantasy Analysis API for data and analysis. Make sure the backend API is running and accessible at the URL specified in your `.env.local` file.

## Building for Production

To build the application for production:

```bash
pnpm build
```

To run the production build locally:

```bash
pnpm start
```

## Contributing

1. Follow the code style guidelines in the main project
2. Write clean, maintainable, and testable code
3. Update documentation as needed
4. Test your changes thoroughly before submitting a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.