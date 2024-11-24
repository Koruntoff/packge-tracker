<!-- frontend/src/routes/+layout.svelte -->
<script>
  import "../app.css";
  import Dashboard from './+page.svelte';
  import Scan from './scan/+page.svelte';
  import Customers from './customers/+page.svelte';
  import Schedule from './schedule/+page.svelte';
  
  let activeTab = window.location.pathname;
  let currentComponent;

  const navItems = [
    { name: 'Dashboard', path: '/', component: Dashboard },
    { name: 'Package', path: '/scan', component: Scan },
    { name: 'Customers', path: '/customers', component: Customers },
    { name: 'Schedule', path: '/schedule', component: Schedule },
  ];

  const handleNavigation = (path) => {
    activeTab = path;
    history.pushState(null, '', path);
    updateComponent(path);
  };

  const updateComponent = (path) => {
    const route = navItems.find(item => item.path === path) || navItems[0];
    currentComponent = route.component;
  };

  // Initialize component on page load
  updateComponent(activeTab);
</script>

<div class="min-h-screen bg-gradient-to-b from-purple-950 to-purple-900">
  <div class="flex h-screen">
    <div class="w-64 bg-purple-950 px-4 py-6">
      <div class="mb-8">
        <h1 class="text-xl font-semibold text-white px-2">MailRoom Manager</h1>
      </div>
      <nav class="space-y-1">
        {#each navItems as item}
          <button
            on:click={() => handleNavigation(item.path)}
            class="w-full flex items-center px-3 py-2 text-sm rounded-md transition-colors {activeTab === item.path ? 'bg-purple-800/50 text-white' : 'text-purple-300 hover:bg-purple-800/30 hover:text-white'}"
          >
            <span>{item.name}</span>
          </button>
        {/each}
      </nav>
    </div>

    <div class="flex-1 overflow-auto">
      {#if currentComponent}
        <svelte:component this={currentComponent} />
      {:else}
        <div class="p-8 text-white">Page not found</div>
      {/if}
    </div>
  </div>
</div>