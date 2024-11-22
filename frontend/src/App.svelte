<script>
  import { onMount } from 'svelte';
  import { format } from 'date-fns';

  let stats = {
    totalPackages: 0,
    pendingDeliveries: 0,
    totalCustomers: 0,
    availableLocations: 0
  };

  let recentPackages = [];
  let activeTab = 'dashboard';

  onMount(async () => {
    try {
      // Fetch dashboard data
      const response = await fetch('http://localhost:8000/api/dashboard/');
      const data = await response.json();
      stats = data.stats;
      recentPackages = data.recent_packages;
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  });
</script>

<div class="min-h-screen bg-gradient-to-b from-purple-950 to-purple-900">
  <!-- Navigation -->
  <div class="flex h-screen">
    <!-- Sidebar -->
    <div class="w-64 bg-purple-950 px-4 py-6">
      <div class="mb-8">
        <h1 class="text-xl font-semibold text-white px-2">MailRoom Manager</h1>
      </div>
      <nav class="space-y-1">
        {#each ['Dashboard', 'Scan Package', 'Customers', 'Locations', 'Schedule'] as tab}
          <a
            href={tab === 'Dashboard' ? '/' : `/${tab.toLowerCase().replace(' ', '')}`}
            class="flex items-center px-3 py-2 text-sm rounded-md transition-colors
              {activeTab === tab.toLowerCase() ? 'bg-purple-800/50 text-white' : 'text-purple-300 hover:bg-purple-800/30 hover:text-white'}"
          >
            <span>{tab}</span>
          </a>
        {/each}
      </nav>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-auto">
      <!-- Top Header -->
      <div class="bg-purple-950 border-b border-white/10">
        <div class="flex items-center justify-between px-8 py-4">
          <div class="flex items-center space-x-4">
            <div class="relative">
              <input
                type="text"
                placeholder="Search..."
                class="pl-10 pr-4 py-2 bg-white/5 rounded-md text-white placeholder-purple-300 focus:outline-none focus:ring-1 focus:ring-purple-400 w-64"
              />
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <button class="p-2 text-purple-300 hover:text-white transition-colors">
              <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </button>
            <div class="h-8 w-8 bg-purple-800 rounded-full"></div>
          </div>
        </div>
      </div>

      <main class="p-8">
        <!-- Stats Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div class="bg-white/10 rounded-lg p-6">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <svg class="h-6 w-6 text-purple-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
                </svg>
              </div>
              <div class="ml-5">
                <p class="text-purple-200 text-sm">Total Packages</p>
                <p class="text-2xl font-semibold text-white">{stats.totalPackages}</p>
              </div>
            </div>
          </div>

          <!-- Repeat similar structure for other stats -->
          <!-- Recent Packages Table -->
          <div class="bg-white/10 rounded-lg p-6 col-span-4">
            <h2 class="text-lg font-semibold text-white mb-4">Recent Packages</h2>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-purple-800">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase tracking-wider">Tracking Number</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase tracking-wider">Customer</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase tracking-wider">Location</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase tracking-wider">Status</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase tracking-wider">Arrival Date</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-purple-800">
                  {#each recentPackages as pkg}
                    <tr class="text-purple-200">
                      <td class="px-6 py-4 whitespace-nowrap">{pkg.tracking_number}</td>
                      <td class="px-6 py-4 whitespace-nowrap">{pkg.customer_name}</td>
                      <td class="px-6 py-4 whitespace-nowrap">{pkg.location_code}</td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        <span class={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                          ${pkg.status === 'delivered' ? 'bg-green-900 text-green-200' : 
                            pkg.status === 'pending' ? 'bg-yellow-900 text-yellow-200' : 
                            'bg-purple-800 text-purple-200'}`}>
                          {pkg.status}
                        </span>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap">
                        {format(new Date(pkg.arrival_date), 'MMM dd, yyyy')}
                      </td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </main>
    </div>
  </div>
</div>