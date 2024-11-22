<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    
    let customers = [];
    let searchTerm = '';
    let showAddModal = false;
    let newCustomer = {
      name: '',
      email: '',
      phone: '',
      address: ''
    };
  
    $: filteredCustomers = customers.filter(customer => 
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase())
    );
  
    onMount(async () => {
      try {
        const response = await fetch('http://localhost:8000/api/customers/');
        customers = await response.json();
      } catch (error) {
        console.error('Error fetching customers:', error);
      }
    });
  
    async function handleAddCustomer() {
      try {
        const response = await fetch('http://localhost:8000/api/customers/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newCustomer)
        });
  
        if (response.ok) {
          const addedCustomer = await response.json();
          customers = [...customers, addedCustomer];
          showAddModal = false;
          newCustomer = { name: '', email: '', phone: '', address: '' };
        }
      } catch (error) {
        console.error('Error adding customer:', error);
      }
    }
  </script>
  
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Customers</h1>
      <button
        on:click={() => showAddModal = true}
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Add Customer
      </button>
    </div>
  
    <!-- Search -->
    <div class="max-w-xl">
      <input
        type="text"
        bind:value={searchTerm}
        placeholder="Search customers..."
        class="w-full px-4 py-2 border rounded-md"
      />
    </div>
  
    <!-- Customer List -->
    <div class="bg-white shadow overflow-hidden sm:rounded-md">
      <ul class="divide-y divide-gray-200">
        {#each filteredCustomers as customer (customer.id)}
          <li transition:fade>
            <div class="px-4 py-4 sm:px-6">
              <div class="flex items-center justify-between">
                <div class="flex-1">
                  <h3 class="text-lg font-medium text-gray-900">{customer.name}</h3>
                  <p class="text-sm text-gray-500">{customer.email}</p>
                  <p class="text-sm text-gray-500">{customer.phone}</p>
                </div>
                <div class="flex space-x-2">
                  <button class="text-blue-600 hover:text-blue-800">Edit</button>
                  <button class="text-red-600 hover:text-red-800">Delete</button>
                </div>
              </div>
            </div>
          </li>
        {/each}
      </ul>
    </div>
  
    <!-- Add Customer Modal -->
    {#if showAddModal}
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h2 class="text-xl font-bold mb-4">Add New Customer</h2>
          <form on:submit|preventDefault={handleAddCustomer} class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Name</label>
              <input
                type="text"
                bind:value={newCustomer.name}
                class="mt-1 w-full border rounded-md px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                bind:value={newCustomer.email}
                class="mt-1 w-full border rounded-md px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Phone</label>
              <input
                type="tel"
                bind:value={newCustomer.phone}
                class="mt-1 w-full border rounded-md px-3 py-2"
                required
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Address</label>
              <textarea
                bind:value={newCustomer.address}
                class="mt-1 w-full border rounded-md px-3 py-2"
                rows="3"
                required
              ></textarea>
            </div>
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                on:click={() => showAddModal = false}
                class="px-4 py-2 border rounded-md"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Add Customer
              </button>
            </div>
          </form>
        </div>
      </div>
    {/if}
  </div>