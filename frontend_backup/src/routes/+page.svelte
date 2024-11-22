<script>
    import { onMount } from 'svelte';
  
    let stats = {
      pendingPackages: 0,
      totalCustomers: 0,
      availableLocations: 0,
      unpaidInvoices: 0
    };
  
    let recentPackages = [];
    let todaySchedule = [];
  
    onMount(async () => {
      try {
        // Fetch statistics and data from your API
        const statsResponse = await fetch('http://localhost:8000/api/packages/stats/');
        const packagesResponse = await fetch('http://localhost:8000/api/packages/?status=pending');
        const scheduleResponse = await fetch('http://localhost:8000/api/schedule/today/');
  
        stats = await statsResponse.json();
        recentPackages = await packagesResponse.json();
        todaySchedule = await scheduleResponse.json();
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      }
    });
  </script>
  
  <div class="space-y-6">
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <dt class="text-sm font-medium text-gray-500 truncate">Pending Packages</dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">{stats.pendingPackages}</dd>
        </div>
      </div>
      
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <dt class="text-sm font-medium text-gray-500 truncate">Total Customers</dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">{stats.totalCustomers}</dd>
        </div>
      </div>
  
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <dt class="text-sm font-medium text-gray-500 truncate">Available Locations</dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">{stats.availableLocations}</dd>
        </div>
      </div>
  
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <dt class="text-sm font-medium text-gray-500 truncate">Unpaid Invoices</dt>
          <dd class="mt-1 text-3xl font-semibold text-gray-900">{stats.unpaidInvoices}</dd>
        </div>
      </div>
    </div>
  
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Recent Packages -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-lg font-medium text-gray-900">Recent Packages</h2>
          <div class="mt-4 flow-root">
            <ul class="divide-y divide-gray-200">
              {#each recentPackages as package}
                <li class="py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {package.tracking_number}
                      </p>
                      <p class="text-sm text-gray-500 truncate">
                        {package.customer_name}
                      </p>
                    </div>
                    <div class="inline-flex items-center text-sm text-gray-500">
                      {package.location_code}
                    </div>
                  </div>
                </li>
              {/each}
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Today's Schedule -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h2 class="text-lg font-medium text-gray-900">Today's Schedule</h2>
          <div class="mt-4 flow-root">
            <ul class="divide-y divide-gray-200">
              {#each todaySchedule as event}
                <li class="py-4">
                  <div class="flex items-center space-x-4">
                    <div class="flex-1 min-w-0">
                      <p class="text-sm font-medium text-gray-900 truncate">
                        {event.title}
                      </p>
                      <p class="text-sm text-gray-500">
                        {new Date(event.start_time).toLocaleTimeString()} - 
                        {new Date(event.end_time).toLocaleTimeString()}
                      </p>
                    </div>
                    <div class="inline-flex items-center text-sm text-gray-500">
                      {event.staff_name}
                    </div>
                  </div>
                </li>
              {/each}
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>