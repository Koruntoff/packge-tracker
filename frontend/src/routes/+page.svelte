<script>
  import { onMount } from 'svelte';

  let upcomingEvents = [];
  let recentPackages = [];
  let urgentPickups = [];
  
  // Helper functions for date formatting and comparison
  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('en-US', {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (date) => {
    return new Date(date).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  const isToday = (dateString) => {
    const date = new Date(dateString);
    const today = new Date();
    return date.getDate() === today.getDate() &&
      date.getMonth() === today.getMonth() &&
      date.getFullYear() === today.getFullYear();
  };

  const isTomorrow = (dateString) => {
    const date = new Date(dateString);
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return date.getDate() === tomorrow.getDate() &&
      date.getMonth() === tomorrow.getMonth() &&
      date.getFullYear() === tomorrow.getFullYear();
  };

  const fetchDashboardData = async () => {
    try {
      const [eventsRes, packagesRes] = await Promise.all([
        fetch('http://localhost:8000/api/scheduled-events/'),
        fetch('http://localhost:8000/api/packages/')
      ]);
      
      const events = await eventsRes.json();
      const packages = await packagesRes.json();
      
      // Filter for upcoming events (next 7 days)
      const sevenDaysFromNow = new Date();
      sevenDaysFromNow.setDate(sevenDaysFromNow.getDate() + 7);
      
      upcomingEvents = events
        .filter(event => new Date(event.start_time) <= sevenDaysFromNow)
        .slice(0, 5);
      
      // Get recent packages
      recentPackages = packages
        .filter(pkg => pkg.status === 'received')
        .sort((a, b) => new Date(b.arrival_date) - new Date(a.arrival_date))
        .slice(0, 5);
      
      // Get packages needing urgent pickup (over 5 days old)
      const fiveDaysAgo = new Date();
      fiveDaysAgo.setDate(fiveDaysAgo.getDate() - 5);
      
      urgentPickups = packages
        .filter(pkg => {
          return pkg.status === 'received' && new Date(pkg.arrival_date) < fiveDaysAgo;
        })
        .slice(0, 3);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    }
  };

  const getEventSymbol = (eventType) => {
    switch(eventType) {
      case 'package_delivery':
        return '📦';
      case 'package_pickup':
        return '🚚';
      case 'exhibitor':
        return '📅';
      default:
        return '🔔';
    }
  };

  const getEventColor = (eventType) => {
    switch(eventType) {
      case 'package_delivery':
        return 'bg-green-100 text-green-800';
      case 'package_pickup':
        return 'bg-blue-100 text-blue-800';
      case 'exhibitor':
        return 'bg-purple-100 text-purple-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const formatEventDate = (dateString) => {
    const date = new Date(dateString);
    if (isToday(dateString)) {
      return `Today at ${formatTime(date)}`;
    } else if (isTomorrow(dateString)) {
      return `Tomorrow at ${formatTime(date)}`;
    }
    return `${formatDate(date)}, ${formatTime(date)}`;
  };

  onMount(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 300000);
    return () => clearInterval(interval);
  });
</script>

<div class="p-6 space-y-6">
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <!-- Upcoming Events Card -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="flex items-center justify-between p-4 border-b">
        <h2 class="text-xl font-bold text-gray-900">Upcoming Events</h2>
        <span class="text-xl">📅</span>
      </div>
      <div class="p-4">
        <div class="space-y-4">
          {#if upcomingEvents.length === 0}
            <p class="text-gray-500 text-center py-4">No upcoming events</p>
          {:else}
            {#each upcomingEvents as event}
              <div class="flex items-start space-x-4 p-3 rounded-lg hover:bg-gray-50">
                <div class={`p-2 rounded-full ${getEventColor(event.event_type)}`}>
                  <span class="text-lg">{getEventSymbol(event.event_type)}</span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900 truncate">
                    {event.title}
                  </p>
                  <div class="mt-1 flex items-center space-x-2 text-sm text-gray-500">
                    <span>⏰</span>
                    <span>{formatEventDate(event.start_time)}</span>
                  </div>
                  {#if event.location}
                    <div class="mt-1 flex items-center space-x-2 text-sm text-gray-500">
                      <span>📍</span>
                      <span>{event.location}</span>
                    </div>
                  {/if}
                </div>
              </div>
            {/each}
          {/if}
        </div>
      </div>
    </div>

    <!-- Recent Packages Card -->
    <div class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="flex items-center justify-between p-4 border-b">
        <h2 class="text-xl font-bold text-gray-900">Recently Received Packages</h2>
        <span class="text-xl">📦</span>
      </div>
      <div class="p-4">
        <div class="space-y-4">
          {#if recentPackages.length === 0}
            <p class="text-gray-500 text-center py-4">No recent packages</p>
          {:else}
            {#each recentPackages as pkg}
              <div class="flex items-start space-x-4 p-3 rounded-lg hover:bg-gray-50">
                <div class="p-2 rounded-full bg-blue-100 text-blue-800">
                  <span class="text-lg">📦</span>
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm font-medium text-gray-900">
                    {pkg.customer_name}
                  </p>
                  <p class="mt-1 text-sm text-gray-500">
                    {pkg.tracking_number}
                  </p>
                  <div class="mt-1 flex items-center space-x-2 text-sm text-gray-500">
                    <span>⏰</span>
                    <span>Received {formatEventDate(pkg.arrival_date)}</span>
                  </div>
                  <div class="mt-1 flex items-center space-x-2 text-sm text-gray-500">
                    <span>📍</span>
                    <span>Shelf {pkg.shelf_number}</span>
                  </div>
                </div>
              </div>
            {/each}
          {/if}
        </div>
      </div>
    </div>
  </div>

  <!-- Urgent Pickups Card -->
  {#if urgentPickups.length > 0}
    <div class="bg-red-50 rounded-lg shadow-md overflow-hidden">
      <div class="flex items-center justify-between p-4 border-b border-red-100">
        <h2 class="text-xl font-bold text-red-800">Urgent Pickups Required</h2>
        <span class="text-xl">⚠️</span>
      </div>
      <div class="p-4">
        <div class="space-y-4">
          {#each urgentPickups as pkg}
            <div class="flex items-start space-x-4 p-3 rounded-lg bg-white">
              <div class="p-2 rounded-full bg-red-100 text-red-800">
                <span class="text-lg">📦</span>
              </div>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900">
                  {pkg.customer_name}
                </p>
                <p class="mt-1 text-sm text-gray-500">
                  {pkg.tracking_number}
                </p>
                <div class="mt-1 flex items-center space-x-2 text-sm text-red-600">
                  <span>⏰</span>
                  <span>Waiting since {formatDate(pkg.arrival_date)}</span>
                </div>
              </div>
            </div>
          {/each}
        </div>
      </div>
    </div>
  {/if}
</div>