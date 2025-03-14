import React from "react";

export default function DriversPage() {
  // This would normally be fetched from the API
  const drivers = [
    {
      id: 1,
      name: "Max Verstappen",
      team: "Red Bull Racing",
      price: 30.5,
      points: 51,
      valueRatio: 1.67,
    },
    {
      id: 2,
      name: "Charles Leclerc",
      team: "Ferrari",
      price: 25.8,
      points: 47,
      valueRatio: 1.82,
    },
    {
      id: 3,
      name: "Sergio Perez",
      team: "Red Bull Racing",
      price: 20.2,
      points: 36,
      valueRatio: 1.78,
    },
    {
      id: 4,
      name: "Carlos Sainz",
      team: "Ferrari",
      price: 19.5,
      points: 33,
      valueRatio: 1.69,
    },
    {
      id: 5,
      name: "Lewis Hamilton",
      team: "Mercedes",
      price: 23.0,
      points: 19,
      valueRatio: 0.83,
    },
    {
      id: 6,
      name: "Lando Norris",
      team: "McLaren",
      price: 18.5,
      points: 16,
      valueRatio: 0.86,
    },
    {
      id: 7,
      name: "George Russell",
      team: "Mercedes",
      price: 21.0,
      points: 19,
      valueRatio: 0.90,
    },
    {
      id: 8,
      name: "Oscar Piastri",
      team: "McLaren",
      price: 15.0,
      points: 12,
      valueRatio: 0.80,
    },
    {
      id: 9,
      name: "Fernando Alonso",
      team: "Aston Martin",
      price: 16.5,
      points: 10,
      valueRatio: 0.61,
    },
    {
      id: 10,
      name: "Lance Stroll",
      team: "Aston Martin",
      price: 12.0,
      points: 10,
      valueRatio: 0.83,
    },
  ];

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">F1 Drivers</h1>
        <p className="text-gray-600">
          View and analyze Formula 1 drivers and their fantasy performance
        </p>
      </div>

      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Driver
                </th>
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
              {drivers.map((driver) => (
                <tr key={driver.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="font-medium text-gray-900">{driver.name}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-500">{driver.team}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{driver.price.toFixed(1)}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm text-gray-900">{driver.points}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className={`text-sm ${driver.valueRatio >= 1.0 ? 'text-green-600' : 'text-red-600'}`}>
                      {driver.valueRatio.toFixed(2)}
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-4">Driver Value Analysis</h2>
        <p className="mb-4">
          The value ratio indicates how many points a driver scores per million dollars of their price.
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
    </div>
  );
} 