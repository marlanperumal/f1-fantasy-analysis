import React from "react";

export default function TeamsPage() {
  // This would normally be fetched from the API
  const teams = [
    {
      id: 1,
      name: "Red Bull Racing",
      price: 32.5,
      points: 87,
      valueRatio: 2.68,
    },
    {
      id: 2,
      name: "Ferrari",
      price: 30.0,
      points: 80,
      valueRatio: 2.67,
    },
    {
      id: 3,
      name: "Mercedes",
      price: 27.5,
      points: 38,
      valueRatio: 1.38,
    },
    {
      id: 4,
      name: "McLaren",
      price: 25.0,
      points: 28,
      valueRatio: 1.12,
    },
    {
      id: 5,
      name: "Aston Martin",
      price: 20.0,
      points: 20,
      valueRatio: 1.00,
    },
    {
      id: 6,
      name: "Alpine",
      price: 15.0,
      points: 8,
      valueRatio: 0.53,
    },
    {
      id: 7,
      name: "Williams",
      price: 10.0,
      points: 6,
      valueRatio: 0.60,
    },
    {
      id: 8,
      name: "RB",
      price: 8.5,
      points: 4,
      valueRatio: 0.47,
    },
    {
      id: 9,
      name: "Haas F1 Team",
      price: 7.5,
      points: 1,
      valueRatio: 0.13,
    },
    {
      id: 10,
      name: "Sauber",
      price: 7.0,
      points: 0,
      valueRatio: 0.00,
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">F1 Teams</h1>
        <p className="text-gray-600">
          View and analyze Formula 1 teams and their fantasy performance
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Team
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Price (M$)
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Points
                </th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Value Ratio
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {teams.map((team) => (
                <tr key={team.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="font-medium text-gray-900">{team.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{team.price.toFixed(1)}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{team.points}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm ${team.valueRatio >= 1.0 ? 'text-green-600' : 'text-red-600'}`}>
                      {team.valueRatio.toFixed(2)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Team Value Analysis</h2>
          <p className="mb-4">
            The value ratio indicates how many points a team scores per million dollars of their price.
            A higher value ratio means better value for money.
          </p>
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              <div className="w-4 h-4 bg-green-600 rounded-full mr-2"></div>
              <span className="text-sm">Good value (≥ 1.0)</span>
            </div>
            <div className="flex items-center">
              <div className="w-4 h-4 bg-red-600 rounded-full mr-2"></div>
              <span className="text-sm">Poor value (&lt; 1.0)</span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Team Selection Tips</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>You can select up to 2 teams for your fantasy lineup</li>
            <li>Top teams are more expensive but generally score more points</li>
            <li>Consider balancing high-performing teams with value picks</li>
            <li>Team performance can vary significantly by track type</li>
            <li>Monitor team upgrades and development throughout the season</li>
          </ul>
        </div>
      </div>
    </div>
  );
} 