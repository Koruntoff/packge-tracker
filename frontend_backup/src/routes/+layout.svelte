<script>
    import "../app.css";
    import { page } from "$app/stores";
  </script>
  
  <div class="min-h-screen bg-gray-100">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between h-16">
          <div class="flex">
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-bold text-gray-800">MailRoom Manager</span>
            </div>
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <a href="/" 
                class="border-b-2 {$page.url.pathname === '/' ? 'border-blue-500' : 'border-transparent'} 
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Dashboard
              </a>
              <a href="/packages"
                class="border-b-2 {$page.url.pathname.startsWith('/packages') ? 'border-blue-500' : 'border-transparent'}
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Packages
              </a>
              <a href="/customers"
                class="border-b-2 {$page.url.pathname.startsWith('/customers') ? 'border-blue-500' : 'border-transparent'}
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Customers
              </a>
              <a href="/locations"
                class="border-b-2 {$page.url.pathname.startsWith('/locations') ? 'border-blue-500' : 'border-transparent'}
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Locations
              </a>
              <a href="/invoices"
                class="border-b-2 {$page.url.pathname.startsWith('/invoices') ? 'border-blue-500' : 'border-transparent'}
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Invoices
              </a>
              <a href="/schedule"
                class="border-b-2 {$page.url.pathname.startsWith('/schedule') ? 'border-blue-500' : 'border-transparent'}
                       text-gray-900 inline-flex items-center px-1 pt-1">
                Schedule
              </a>
            </div>
          </div>
        </div>
      </div>
    </nav>
  
    <!-- Page Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <slot />
    </main>
  </div>