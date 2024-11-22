<script>
    import "../app.css";
    import { page } from '$app/stores';
  
    $: activeTab = $page.url.pathname;
  
    const navItems = [
      { name: 'Dashboard', path: '/' },
      { name: 'Scan Package', path: '/scan' },
      { name: 'Customers', path: '/customers' },
      { name: 'Locations', path: '/locations' },
      { name: 'Schedule', path: '/schedule' }
    ];
  </script>
  
  <div class="min-h-screen bg-gradient-to-b from-purple-950 to-purple-900">
    <div class="flex h-screen">
      <!-- Sidebar -->
      <div class="w-64 bg-purple-950 px-4 py-6">
        <div class="mb-8">
          <h1 class="text-xl font-semibold text-white px-2">MailRoom Manager</h1>
        </div>
        <nav class="space-y-1">
          {#each navItems as item}
            <a
              href={item.path}
              class="w-full flex items-center px-3 py-2 text-sm rounded-md transition-colors
                {activeTab === item.path ? 'bg-purple-800/50 text-white' : 'text-purple-300 hover:bg-purple-800/30 hover:text-white'}"
            >
              <span>{item.name}</span>
            </a>
          {/each}
        </nav>
      </div>
  
      <!-- Main Content -->
      <div class="flex-1 overflow-auto">
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
  
        <!-- Page Content -->
        <slot />
      </div>
    </div>
  </div>