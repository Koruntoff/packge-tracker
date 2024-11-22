<script>
    import { onMount } from 'svelte';
    import { format } from 'date-fns';
  
    let invoices = [];
    let searchTerm = '';
    let sortBy = 'issued_date';
    let sortDirection = 'desc';
    let showCreateModal = false;
    let selectedCustomer = null;
    let selectedPackages = [];
    let customers = [];
    let availablePackages = [];
  
    $: filteredInvoices = invoices
      .filter(invoice => 
        invoice.customer_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        invoice.id.toString().includes(searchTerm)
      )
      .sort((a, b) => {
        const factor = sortDirection === 'asc' ? 1 : -1;
        return factor * (a[sortBy] > b[sortBy] ? 1 : -1);
      });
  
    onMount(async () => {
      try {
        const [invoicesRes, customersRes] = await Promise.all([
          fetch('http://localhost:8000/api/invoices/'),
          fetch('http://localhost:8000/api/customers/')
        ]);
        invoices = await invoicesRes.json();
        customers = await customersRes.json();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });
  
    async function handleCustomerSelect(event) {
      const customerId = event.target.value;
      if (customerId) {
        try {
          const response = await fetch(`http://localhost:8000/api/customers/${customerId}/packages/`);
          availablePackages = await response.json();
        } catch (error) {
          console.error('Error fetching packages:', error);
        }
      }
    }
  
    async function createInvoice() {
      const invoiceData = {
        customer: selectedCustomer,
        packages: selectedPackages,
        due_date: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
        total_amount: calculateTotal(selectedPackages)
      };
  
      try {
        const response = await fetch('http://localhost:8000/api/invoices/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(invoiceData)
        });
  
        if (response.ok) {
          const newInvoice = await response.json();
          invoices = [...invoices, newInvoice];
          showCreateModal = false;
        }
      } catch (error) {
        console.error('Error creating invoice:', error);
      }
    }
  
    function calculateTotal(packages) {
      // Add your pricing logic here
      return packages.reduce((total, pkg) => total + (pkg.weight * 10), 0);
    }
  
    async function downloadInvoice(invoiceId) {
      try {
        const response = await fetch(`http://localhost:8000/api/invoices/${invoiceId}/pdf/`);
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `invoice-${invoiceId}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } catch (error) {
        console.error('Error downloading invoice:', error);
      }
    }
  </script>
  
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900">Invoices</h1>
      <button
        on:click={() => showCreateModal = true}
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Create Invoice
      </button>
    </div>
  
    <div class="flex space-x-4">
      <input
        type="text"
        bind:value={searchTerm}
        placeholder="Search invoices..."
        class="flex-1 px-4 py-2 border rounded-md"
      />
      <select
        bind:value={sortBy}
        class="px-4 py-2 border rounded-md"
      >
        <option value="issued_date">Issue Date</option>
        <option value="due_date">Due Date</option>
        <option value="total_amount">Amount</option>
      </select>
      <button
        on:click={() => sortDirection = sortDirection === 'asc' ? 'desc' : 'asc'}
        class="px-4 py-2 border rounded-md"
      >
        {sortDirection === 'asc' ? '↑' : '↓'}
      </button>
    </div>
  
    <div class="bg-white shadow overflow-hidden sm:rounded-lg">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Invoice #
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Customer
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Amount
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Status
            </th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Due Date
            </th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          {#each filteredInvoices as invoice}
            <tr>
              <td class="px-6 py-4 whitespace-nowrap">
                #{invoice.id}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {invoice.customer_name}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                ${invoice.total_amount}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  invoice.paid ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                }`}>
                  {invoice.paid ? 'Paid' : 'Pending'}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                {format(new Date(invoice.due_date), 'MMM dd, yyyy')}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <button
                  on:click={() => downloadInvoice(invoice.id)}
                  class="text-blue-600 hover:text-blue-900"
                >
                  Download
                </button>
              </td>
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
  
    {#if showCreateModal}
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center">
        <div class="bg-white rounded-lg p-6 max-w-lg w-full">
          <h2 class="text-xl font-bold mb-4">Create New Invoice</h2>
          <form on:submit|preventDefault={createInvoice} class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">Customer</label>
              <select
                bind:value={selectedCustomer}
                on:change={handleCustomerSelect}
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
                required
              >
                <option value="">Select customer...</option>
                {#each customers as customer}
                  <option value={customer.id}>{customer.name}</option>
                {/each}
              </select>
            </div>
  
            {#if availablePackages.length > 0}
              <div>
                <label class="block text-sm font-medium text-gray-700">Packages</label>
                <div class="mt-2 space-y-2">
                  {#each availablePackages as pkg}
                    <label class="flex items-center">
                      <input
                        type="checkbox"
                        value={pkg.id}
                        bind:group={selectedPackages}
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <span class="ml-2">
                        {pkg.tracking_number} ({pkg.weight}kg)
                      </span>
                    </label>
                  {/each}
                </div>
              </div>
            {/if}
  
            <div class="flex justify-end space-x-3">
              <button
                type="button"
                on:click={() => showCreateModal = false}
                class="px-4 py-2 border rounded-md"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Create Invoice
              </button>
            </div>
          </form>
        </div>
      </div>
    {/if}
  </div>