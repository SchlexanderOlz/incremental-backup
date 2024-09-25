import { Bar } from 'react-chartjs-2'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { HardDrive, Settings } from 'lucide-react'
import { formatDistance } from 'date-fns'
import { de } from 'date-fns/locale'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

function humanFileSize(size: number) {
  var i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
  return +((size / Math.pow(1024, i)).toFixed(2)) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
}

export default function Dashboard() {
  // This is the data coming from API
  const data = {
    lastBackup: new Date(), // Datetime Object
    usedStorage: 0, // Size used in Bytes
    maxStorage: 100000000, // Max size in Bytes
    backups: [ // Backup List
      { name: "Backup-01", date: new Date(2024, 8, 24, 8) },
      { name: "Backup-02", date: new Date(2024, 8, 23, 10) }
    ],
    dailySizes: { // More Statistics
      'Mon': 0,
      'Tue': 0,
      'Wed': 0,
      'Thu': 0,
      'Fri': 0,
      'Sat': 0,
      'Sun': 0,
    }
  }

  const chartData = {
    labels: Object.keys(data.dailySizes),
    datasets: [
      {
        label: 'Backup Size (GB)',
        data: Object.values(data.dailySizes),
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

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm z-10">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8 flex justify-between items-center">
            <h1 className="text-2xl font-semibold text-gray-900">Incrementify</h1>
          </div>
        </header>

        {/* Main content */}
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100">
          <div className="container mx-auto px-6 py-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
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
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Storage Used</CardTitle>
                  <Settings className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{humanFileSize(data.usedStorage)}</div>
                  <p className="text-xs text-muted-foreground">of {humanFileSize(data.maxStorage)}</p>
                  <Progress value={(data.usedStorage / data.maxStorage) * 100} className="mt-2" />
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Backups</CardTitle>
                  <HardDrive className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">0</div>
                  <p className="text-xs text-muted-foreground">+0 today</p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Last Backup</CardTitle>
                  <HardDrive className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{data.lastBackup.toLocaleDateString("de-DE", { hour: "numeric", minute: "numeric" })}</div>
                </CardContent>
              </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle>Recent Backups</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {data.backups.map((backup, idx) => (
                      <li key={idx} className="flex justify-between items-center">
                        <span>{backup.name}</span>
                        <span className="text-sm text-gray-500">{formatDistance(backup.date, Date.now(), { locale: de, includeSeconds: true })}</span>
                      </li>
                    ))}

                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Backup Sizes</CardTitle>
                </CardHeader>
                <CardContent>
                  <Bar data={chartData} options={chartOptions} />
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}