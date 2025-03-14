import React from "react";

export default function SimulatorPage() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">F1 Race Simulator</h1>
        <p className="text-gray-600">
          Simulate race outcomes and predict fantasy points for different scenarios
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Race selection */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Race Selection</h2>
          <div className="space-y-4">
            <div>
              <label htmlFor="race" className="block text-sm font-medium text-gray-700 mb-1">
                Select Race
              </label>
              <select
                id="race"
                className="w-full border border-gray-300 rounded-md px-3 py-2"
                defaultValue="australia"
              >
                <option value="australia">Australian Grand Prix</option>
                <option value="japan">Japanese Grand Prix</option>
                <option value="china">Chinese Grand Prix</option>
                <option value="miami">Miami Grand Prix</option>
                <option value="imola">Emilia Romagna Grand Prix</option>
              </select>
            </div>

            <div>
              <label htmlFor="trackType" className="block text-sm font-medium text-gray-700 mb-1">
                Track Type
              </label>
              <select
                id="trackType"
                className="w-full border border-gray-300 rounded-md px-3 py-2"
                defaultValue="street"
              >
                <option value="street">Street Circuit</option>
                <option value="permanent">Permanent Circuit</option>
                <option value="highSpeed">High-Speed Circuit</option>
                <option value="technical">Technical Circuit</option>
              </select>
            </div>

            <div>
              <label htmlFor="weather" className="block text-sm font-medium text-gray-700 mb-1">
                Weather Conditions
              </label>
              <select
                id="weather"
                className="w-full border border-gray-300 rounded-md px-3 py-2"
                defaultValue="dry"
              >
                <option value="dry">Dry</option>
                <option value="wet">Wet</option>
                <option value="mixed">Mixed Conditions</option>
              </select>
            </div>
          </div>
        </div>

        {/* Driver adjustments */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Driver Adjustments</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Driver Form Adjustments
              </label>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Max Verstappen</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Charles Leclerc</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Lewis Hamilton</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-2">
              <button className="text-sm text-blue-600 hover:underline">
                Adjust more drivers...
              </button>
            </div>
          </div>
        </div>

        {/* Team adjustments */}
        <div className="bg-white p-6 rounded-lg shadow-md">
          <h2 className="text-xl font-bold mb-4">Team Adjustments</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">
                Team Performance Adjustments
              </label>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Red Bull Racing</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Ferrari</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Mercedes</span>
                  <div className="flex items-center">
                    <button className="w-6 h-6 bg-gray-200 rounded-l flex items-center justify-center">-</button>
                    <span className="w-8 text-center">0</span>
                    <button className="w-6 h-6 bg-gray-200 rounded-r flex items-center justify-center">+</button>
                  </div>
                </div>
              </div>
            </div>

            <div className="pt-2">
              <button className="text-sm text-blue-600 hover:underline">
                Adjust more teams...
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8 flex justify-center">
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg text-lg font-medium hover:bg-blue-700">
          Run Simulation
        </button>
      </div>

      <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
        <h2 className="text-xl font-bold mb-6">Simulation Results</h2>
        
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Predicted Race Finish</h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Position
                  </th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Driver
                  </th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Team
                  </th>
                  <th scope="col" className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fantasy Points
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {[
                  { pos: 1, driver: "Max Verstappen", team: "Red Bull Racing", points: 25 },
                  { pos: 2, driver: "Charles Leclerc", team: "Ferrari", points: 18 },
                  { pos: 3, driver: "Sergio Perez", team: "Red Bull Racing", points: 15 },
                  { pos: 4, driver: "Carlos Sainz", team: "Ferrari", points: 12 },
                  { pos: 5, driver: "Lewis Hamilton", team: "Mercedes", points: 10 },
                ].map((result) => (
                  <tr key={result.pos} className="hover:bg-gray-50">
                    <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">
                      {result.pos}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {result.driver}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                      {result.team}
                    </td>
                    <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-900">
                      {result.points}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold mb-3">Team Performance</h3>
            <div className="space-y-2">
              {[
                { team: "Red Bull Racing", points: 40 },
                { team: "Ferrari", points: 30 },
                { team: "Mercedes", points: 15 },
                { team: "McLaren", points: 10 },
                { team: "Aston Martin", points: 5 },
              ].map((team, index) => (
                <div key={index} className="flex justify-between items-center">
                  <span className="text-sm">{team.team}</span>
                  <span className="text-sm font-medium">{team.points} pts</span>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h3 className="font-semibold mb-3">Fantasy Team Impact</h3>
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm mb-2">Your optimal team would score:</p>
              <p className="text-2xl font-bold text-green-600">128 points</p>
              <div className="mt-4 text-sm text-gray-600">
                <p>Top performing drivers:</p>
                <ul className="list-disc pl-5 mt-1 space-y-1">
                  <li>Max Verstappen: 25 pts</li>
                  <li>Charles Leclerc: 18 pts</li>
                  <li>Sergio Perez: 15 pts</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="font-semibold mb-3">Simulation Notes</h3>
          <p className="text-sm text-gray-600">
            This simulation is based on historical performance data, current form, and the specific
            characteristics of the Australian Grand Prix. Weather conditions and other race-day
            factors can significantly impact actual results.
          </p>
        </div>
      </div>
    </div>
  );
} 