import { useState } from 'react'
import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { Bell, HardDrive, Menu, Settings, User } from 'lucide-react'

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  const chartData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Backup Size (GB)',
        data: [2, 5, 3, 4, 6, 2, 1],
        backgroundColor: 'rgba(59, 130, 246, 0.5)',
      },
    ],
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: 'Backup Sizes Over Time',
      },
    },
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <aside className={`bg-white w-64 min-h-screen p-4 ${sidebarOpen ? '' : 'hidden'} md:block`}>
        <nav>
          <ul className="space-y-2">
            <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-200 rounded">Dashboard</a></li>
            <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-200 rounded">Backups</a></li>
            <li><a href="#" className="block py-2 px-4 text-gray-700 hover:bg-gray-200 rounded">Settings</a></li>
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm z-10">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-gray-900">Incrementify</h1>
            <div className="flex items-center">
              <Button variant="ghost" size="icon" className="mr-2">
                <Bell className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="mr-2">
                <User className="h-5 w-5" />
              </Button>
              <Button variant="ghost" size="icon" className="md:hidden" onClick={() => setSidebarOpen(!sidebarOpen)}>
                <Menu className="h-5 w-5" />
              </Button>
            </div>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
          <div className="container mx-auto px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Backups</CardTitle>
                  <HardDrive className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">254</div>
                  <p className="text-xs text-muted-foreground">+12 from last week</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Storage Used</CardTitle>
                  <Settings className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1.2 TB</div>
                  <p className="text-xs text-muted-foreground">of 2 TB</p>
                  <Progress value={60} className="mt-2" />
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Last Backup</CardTitle>
                  <HardDrive className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">2 hours ago</div>
                  <p className="text-xs text-muted-foreground">Next backup in 4 hours</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">System Status</CardTitle>
                  <Settings className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold text-green-600">Healthy</div>
                  <p className="text-xs text-muted-foreground">All systems operational</p>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle>Backup Sizes</CardTitle>
                </CardHeader>
                <CardContent>
                  <Bar data={chartData} options={chartOptions} />
                </CardContent>
              </Card>
              <Card>
                <CardHeader>
                  <CardTitle>Recent Backups</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    <li className="flex justify-between items-center">
                      <span>Project A</span>
                      <span className="text-sm text-gray-500">2 hours ago</span>
                    </li>
                    <li className="flex justify-between items-center">
                      <span>Project B</span>
                      <span className="text-sm text-gray-500">5 hours ago</span>
                    </li>
                    <li className="flex justify-between items-center">
                      <span>Project C</span>
                      <span className="text-sm text-gray-500">1 day ago</span>
                    </li>
                    <li className="flex justify-between items-center">
                      <span>Project D</span>
                      <span className="text-sm text-gray-500">2 days ago</span>
                    </li>
                  </ul>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}