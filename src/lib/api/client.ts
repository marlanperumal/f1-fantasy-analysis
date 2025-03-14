// API base URL - this should be configured based on environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// API endpoints
const API_ENDPOINTS = {
  // Basic endpoints
  races: "/api/v1/races",
  drivers: "/api/v1/drivers",
  teams: "/api/v1/teams",
  
  // Analysis endpoints
  driverValue: "/api/v1/analysis/driver-value",
  teamValue: "/api/v1/analysis/team-value",
  formTrends: "/api/v1/analysis/form-trends",
  optimalTeam: "/api/v1/analysis/optimal-team",
  
  // Advanced analysis endpoints
  teamPerformance: "/api/v1/analysis/team-performance",
  pricePointsCorrelation: "/api/v1/analysis/price-points-correlation",
  undervaluedDrivers: "/api/v1/analysis/undervalued-drivers",
  predictPoints: "/api/v1/analysis/predict-points",
  optimalTeamAdvanced: "/api/v1/analysis/optimal-team-advanced",
};

// API client for making requests to the backend
export const apiClient = {
  // Generic fetch function with error handling
  async fetch<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });
      
      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error(`Error fetching from ${endpoint}:`, error);
      throw error;
    }
  },
  
  // Basic data fetching functions
  getRaces: () => apiClient.fetch(API_ENDPOINTS.races),
  getDrivers: () => apiClient.fetch(API_ENDPOINTS.drivers),
  getTeams: () => apiClient.fetch(API_ENDPOINTS.teams),
  
  // Analysis functions
  getDriverValue: () => apiClient.fetch(API_ENDPOINTS.driverValue),
  getTeamValue: () => apiClient.fetch(API_ENDPOINTS.teamValue),
  getFormTrends: () => apiClient.fetch(API_ENDPOINTS.formTrends),
  getOptimalTeam: (budget?: number) => {
    const params = budget ? `?budget=${budget}` : "";
    return apiClient.fetch(`${API_ENDPOINTS.optimalTeam}${params}`);
  },
  
  // Advanced analysis functions
  getTeamPerformance: () => apiClient.fetch(API_ENDPOINTS.teamPerformance),
  getPricePointsCorrelation: () => apiClient.fetch(API_ENDPOINTS.pricePointsCorrelation),
  getUndervaluedDrivers: () => apiClient.fetch(API_ENDPOINTS.undervaluedDrivers),
  getPredictPoints: (driverId: number) => 
    apiClient.fetch(`${API_ENDPOINTS.predictPoints}?driver_id=${driverId}`),
  getOptimalTeamAdvanced: (params: { 
    budget?: number;
    strategy?: "points" | "value" | "balanced";
  } = {}) => {
    const queryParams = new URLSearchParams();
    if (params.budget) queryParams.append("budget", params.budget.toString());
    if (params.strategy) queryParams.append("strategy", params.strategy);
    
    const queryString = queryParams.toString() ? `?${queryParams.toString()}` : "";
    return apiClient.fetch(`${API_ENDPOINTS.optimalTeamAdvanced}${queryString}`);
  },
  
  // Simulation functions
  simulateRace: (params: {
    race: string;
    trackType: string;
    weather: string;
    driverAdjustments?: Record<number, number>;
    teamAdjustments?: Record<number, number>;
  }) => {
    return apiClient.fetch("/api/v1/simulation/race", {
      method: "POST",
      body: JSON.stringify(params),
    });
  },
}; 