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
f1-fantasy-webapp/
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
