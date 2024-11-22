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
  
    onMount(async () => {
      try {
        const response = await fetch('http://localhost:8000/api/dashboard/');
        const data = await response.json();
        stats = data.stats;
        recentPackages = data.recent_packages;
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    });
  </script>
  
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
      <!-- Add other stat cards here -->
    </div>
  
    <!-- Recent Packages Table -->
    <div class="bg-white/10 rounded-lg p-6">
      <h2 class="text-lg font-semibold text-white mb-4">Recent Packages</h2>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-purple-800">
          <!-- Table content -->
        </table>
      </div>
    </div>
  </main>