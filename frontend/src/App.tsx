import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import { HardDrive, Settings, History, Play } from 'lucide-react'
import { formatDistance } from 'date-fns'
import { de } from 'date-fns/locale'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Button } from './components/ui/button'
import { useEffect, useState } from 'react'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

function humanFileSize(size: number) {
  var i = size == 0 ? 0 : Math.floor(Math.log(size) / Math.log(1024));
  return +((size / Math.pow(1024, i)).toFixed(2)) * 1 + ' ' + ['B', 'KB', 'MB', 'GB', 'TB'][i];
}

export default function Dashboard() {
  async function refreshStatus() {
    // Call API to get status and set new state
    // setdata(newData)
    console.log("Refreshing status")
    try {
      const ftch = await fetch("https://sos.com/api/status")
      if (!ftch.ok) {
        console.error("Failed to fetch status")
        setdata({ ...data, healthy: false })
      }
    }
    catch (e) {
      console.error("Failed to fetch status")
      setdata({ ...data, healthy: false })
      return
    }

  }

  type Data = {
    healthy: boolean | undefined,
    lastBackup: Date,
    usedStorage: number,
    maxStorage: number,
    backups: { name: string, date: Date, size: number }[]
  }

  const [backupProgress, setBackupProgress] = useState(0)
  const [isBackupRunning, setIsBackupRunning] = useState(false)
  const [data, setdata] = useState<Data>({
    healthy: undefined, // Boolean
    lastBackup: new Date(), // Datetime Object
    usedStorage: 0, // Size used in Bytes
    maxStorage: 100000000, // Max size in Bytes
    backups: [ // Backup List
      { name: "Backup-01", date: new Date(2024, 8, 24, 8), size: 37218927 },
      { name: "Backup-02", date: new Date(2024, 8, 23, 10), size: 94891 }
    ]
  })

  const startBackup = () => {
    setIsBackupRunning(true)
    setBackupProgress(0)
  }

  useEffect(() => {
    if (isBackupRunning && backupProgress < 100) {
      const timer = setTimeout(() => {
        setBackupProgress(prevProgress => {
          const newProgress = prevProgress + 1
          setdata({ ...data, usedStorage: data.usedStorage += 238329.12 })
          if (newProgress >= 100) {
            setIsBackupRunning(false)
            return 100
          }
          return newProgress
        })
      }, 25)
      return () => clearTimeout(timer)
    }
  }, [isBackupRunning, backupProgress])

  useEffect(() => {
    refreshStatus()
  }, [])

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
                </CardHeader>
                <CardContent>
                  {data.healthy === true && <div className="text-2xl font-bold text-green-600">Healthy</div>}
                  {data.healthy === false && <div className="text-2xl font-bold text-red-600">Unhealthy</div>}
                  {data.healthy === undefined && <div className="text-2xl font-bold text-gray-600">-</div>}
                  <p className="text-xs text-muted-foreground">
                    {data.healthy === true && "All systems operational"}
                    {data.healthy === false && "Leitner is not running"}
                  </p>
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
                  <div className="text-2xl font-bold">
                    {data.lastBackup.getDay() == new Date().getDay()
                      ? data.lastBackup.toLocaleDateString("de-DE", { hour: "numeric", minute: "numeric" }).slice(-5)
                      : data.lastBackup.toLocaleDateString("de-DE", { hour: "numeric", minute: "numeric" })}
                  </div>
                </CardContent>
              </Card>
            </div>

            <div className="flex flex-col lg:flex-row items-stretch justify-center gap-6 mb-8">
              {/* New Backup Action Section */}
              <Card className="flex-1">
                <CardHeader>
                  <CardTitle>Start New Backup</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="flex items-center space-x-4">
                    <Button
                      onClick={startBackup}
                      disabled={isBackupRunning}
                      className="flex items-center space-x-2"
                    >
                      <Play className="h-4 w-4" />
                      <span>Start Backup</span>
                    </Button>
                    <div className="flex-1">
                      <Progress value={backupProgress} className={`w-full`} />
                    </div>
                    <div className="w-16 text-right">{backupProgress}%</div>
                  </div>
                  {isBackupRunning && (
                    <p className="mt-2 text-sm text-muted-foreground">Backup in progress...</p>
                  )}
                  {!isBackupRunning && backupProgress === 100 && (
                    <p className="mt-2 text-sm text-green-600">Backup completed successfully!</p>
                  )}
                </CardContent>
              </Card>

              <Card className='flex-1'>
                <CardHeader>
                  <CardTitle>Recent Backups</CardTitle>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {data.backups.map((backup, idx) => (
                      <li key={idx} className="flex justify-between items-center">
                        <span className="font-semibold">{backup.name}</span>
                        <span>{humanFileSize(backup.size)}</span>
                        <span className="text-sm text-gray-500">vor {formatDistance(backup.date, Date.now(), { locale: de, includeSeconds: true })}</span>
                        <Button variant={"link"}><History /></Button>
                      </li>
                    ))}

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