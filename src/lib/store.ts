import { create } from 'zustand';

// Define the types for our store
interface Driver {
  id: number;
  name: string;
  team: string;
  price: number;
  points: number;
  valueRatio: number;
}

interface Team {
  id: number;
  name: string;
  price: number;
  points: number;
  valueRatio: number;
}

interface FantasyTeam {
  drivers: Driver[];
  teams: Team[];
  totalPrice: number;
  totalPoints: number;
}

interface SimulationSettings {
  race: string;
  trackType: string;
  weather: string;
  driverAdjustments: Record<number, number>;
  teamAdjustments: Record<number, number>;
}

interface AppState {
  // Fantasy team state
  fantasyTeam: FantasyTeam;
  budget: number;
  
  // Simulation state
  simulationSettings: SimulationSettings;
  simulationResults: any | null;
  
  // UI state
  isLoading: boolean;
  activeTab: string;
  
  // Actions
  setFantasyTeam: (team: Partial<FantasyTeam>) => void;
  addDriverToTeam: (driver: Driver) => void;
  removeDriverFromTeam: (driverId: number) => void;
  addTeamToFantasy: (team: Team) => void;
  removeTeamFromFantasy: (teamId: number) => void;
  setBudget: (budget: number) => void;
  setSimulationSettings: (settings: Partial<SimulationSettings>) => void;
  setSimulationResults: (results: any) => void;
  setIsLoading: (isLoading: boolean) => void;
  setActiveTab: (tab: string) => void;
  resetFantasyTeam: () => void;
}

// Create the store
export const useAppStore = create<AppState>((set) => ({
  // Initial state
  fantasyTeam: {
    drivers: [],
    teams: [],
    totalPrice: 0,
    totalPoints: 0,
  },
  budget: 100, // Default budget in millions
  
  simulationSettings: {
    race: 'australia',
    trackType: 'street',
    weather: 'dry',
    driverAdjustments: {},
    teamAdjustments: {},
  },
  simulationResults: null,
  
  isLoading: false,
  activeTab: 'dashboard',
  
  // Actions
  setFantasyTeam: (team) => 
    set((state) => ({
      fantasyTeam: {
        ...state.fantasyTeam,
        ...team,
      },
    })),
  
  addDriverToTeam: (driver) => 
    set((state) => {
      // Check if we already have 5 drivers
      if (state.fantasyTeam.drivers.length >= 5) {
        return state;
      }
      
      // Check if driver is already in the team
      if (state.fantasyTeam.drivers.some(d => d.id === driver.id)) {
        return state;
      }
      
      const newDrivers = [...state.fantasyTeam.drivers, driver];
      const totalPrice = calculateTotalPrice(newDrivers, state.fantasyTeam.teams);
      const totalPoints = calculateTotalPoints(newDrivers, state.fantasyTeam.teams);
      
      return {
        fantasyTeam: {
          ...state.fantasyTeam,
          drivers: newDrivers,
          totalPrice,
          totalPoints,
        },
      };
    }),
  
  removeDriverFromTeam: (driverId) => 
    set((state) => {
      const newDrivers = state.fantasyTeam.drivers.filter(d => d.id !== driverId);
      const totalPrice = calculateTotalPrice(newDrivers, state.fantasyTeam.teams);
      const totalPoints = calculateTotalPoints(newDrivers, state.fantasyTeam.teams);
      
      return {
        fantasyTeam: {
          ...state.fantasyTeam,
          drivers: newDrivers,
          totalPrice,
          totalPoints,
        },
      };
    }),
  
  addTeamToFantasy: (team) => 
    set((state) => {
      // Check if we already have 2 teams
      if (state.fantasyTeam.teams.length >= 2) {
        return state;
      }
      
      // Check if team is already in the fantasy team
      if (state.fantasyTeam.teams.some(t => t.id === team.id)) {
        return state;
      }
      
      const newTeams = [...state.fantasyTeam.teams, team];
      const totalPrice = calculateTotalPrice(state.fantasyTeam.drivers, newTeams);
      const totalPoints = calculateTotalPoints(state.fantasyTeam.drivers, newTeams);
      
      return {
        fantasyTeam: {
          ...state.fantasyTeam,
          teams: newTeams,
          totalPrice,
          totalPoints,
        },
      };
    }),
  
  removeTeamFromFantasy: (teamId) => 
    set((state) => {
      const newTeams = state.fantasyTeam.teams.filter(t => t.id !== teamId);
      const totalPrice = calculateTotalPrice(state.fantasyTeam.drivers, newTeams);
      const totalPoints = calculateTotalPoints(state.fantasyTeam.drivers, newTeams);
      
      return {
        fantasyTeam: {
          ...state.fantasyTeam,
          teams: newTeams,
          totalPrice,
          totalPoints,
        },
      };
    }),
  
  setBudget: (budget) => set({ budget }),
  
  setSimulationSettings: (settings) => 
    set((state) => ({
      simulationSettings: {
        ...state.simulationSettings,
        ...settings,
      },
    })),
  
  setSimulationResults: (results) => set({ simulationResults: results }),
  
  setIsLoading: (isLoading) => set({ isLoading }),
  
  setActiveTab: (tab) => set({ activeTab: tab }),
  
  resetFantasyTeam: () => 
    set({
      fantasyTeam: {
        drivers: [],
        teams: [],
        totalPrice: 0,
        totalPoints: 0,
      },
    }),
}));

// Helper functions
function calculateTotalPrice(drivers: Driver[], teams: Team[]): number {
  const driversPrice = drivers.reduce((sum, driver) => sum + driver.price, 0);
  const teamsPrice = teams.reduce((sum, team) => sum + team.price, 0);
  return driversPrice + teamsPrice;
}

function calculateTotalPoints(drivers: Driver[], teams: Team[]): number {
  const driversPoints = drivers.reduce((sum, driver) => sum + driver.points, 0);
  const teamsPoints = teams.reduce((sum, team) => sum + team.points, 0);
  return driversPoints + teamsPoints;
} 