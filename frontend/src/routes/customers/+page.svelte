<script>
    import { onMount } from 'svelte';
    import { format } from 'date-fns';
  
    let customers = [];
    let searchTerm = '';
    let showAddModal = false;
    let editingCustomer = null;
    let newCustomer = {
      name: '',
      email: '',
      phone: '',
      address: ''
    };
  
    $: filteredCustomers = customers.filter(customer =>
      customer.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      customer.phone.includes(searchTerm)
    );
  
    onMount(async () => {
      await loadCustomers();
    });
  
    async function loadCustomers() {
      try {
        const response = await fetch('http://localhost:8000/api/customers/');
        customers = await response.json();
      } catch (error) {
        console.error('Error loading customers:', error);
      }
    }
  
    async function handleSubmit() {
      try {
        const url = editingCustomer 
          ? `http://localhost:8000/api/customers/${editingCustomer.id}/`
          : 'http://localhost:8000/api/customers/';
        
        const method = editingCustomer ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newCustomer)
        });
  
        if (response.ok) {
          await loadCustomers();
          showAddModal = false;
          editingCustomer = null;
          newCustomer = { name: '', email: '', phone: '', address: '' };
        }
      } catch (error) {
        console.error('Error saving customer:', error);
      }
    }
  
    async function handleDelete(customer) {
      if (confirm(`Are you sure you want to delete ${customer.name}?`)) {
        try {
          const response = await fetch(`http://localhost:8000/api/customers/${customer.id}/`, {
            method: 'DELETE'
          });
  
          if (response.ok) {
            await loadCustomers();
          }
        } catch (error) {
          console.error('Error deleting customer:', error);
        }
      }
    }
  
    function editCustomer(customer) {
      editingCustomer = customer;
      newCustomer = { ...customer };
      showAddModal = true;
    }
  </script>
  
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 sm:px-0 flex justify-between items-center mb-6">
      <h1 class="text-2xl font-bold text-gray-900">Customers</h1>
      <button
        on:click={() => {
          editingCustomer = null;
          newCustomer = { name: '', email: '', phone: '', address: '' };
          showAddModal = true;
        }}
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Add Customer
      </button>
    </div>
  
    <div class="bg-white shadow rounded-lg overflow-hidden">
      <!-- Search -->
      <div class="p-4 border-b">
        <input
          type="text"
          placeholder="Search customers..."
          bind:value={searchTerm}
          class="w-full px-4 py-2 border rounded-md"
        />
      </div>
  
      <!-- Customer List -->
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Email</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Phone</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Address</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            {#each filteredCustomers as customer}
              <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{customer.name}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.email}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{customer.phone}</td>
                <td class="px-6 py-4 text-sm text-gray-500">{customer.address}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    on:click={() => editCustomer(customer)}
                    class="text-blue-600 hover:text-blue-900 mr-4"
                  >
                    Edit
                  </button>
                  <button
                    on:click={() => handleDelete(customer)}
                    class="text-red-600 hover:text-red-900"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    </div>
  </div>
  
  <!-- Add/Edit Modal -->
  {#if showAddModal}
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
      <div class="bg-white rounded-lg p-6 max-w-md w-full">
        <h2 class="text-xl font-bold mb-4">{editingCustomer ? 'Edit' : 'Add'} Customer</h2>
        
        <form on:submit|preventDefault={handleSubmit} class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input
              type="text"
              bind:value={newCustomer.name}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              type="email"
              bind:value={newCustomer.email}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Phone</label>
            <input
              type="tel"
              bind:value={newCustomer.phone}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Address</label>
            <textarea
              bind:value={newCustomer.address}
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            ></textarea>
          </div>
  
          <div class="flex justify-end space-x-3">
            <button
              type="button"
              on:click={() => showAddModal = false}
              class="px-4 py-2 border rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              {editingCustomer ? 'Update' : 'Add'} Customer
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}