<script>
  import { onMount } from 'svelte';
  import BarcodeScanner from '../../lib/components/BarcodeScanner.svelte';
  import { format } from 'date-fns';

  let showScannerModal = false;
  let showAddPackageModal = false;
  let recentPackages = [];
  let scanning = false;
  let locations = []; // Will be fetched from API
  
  // New package form data
  let newPackage = {
    tracking_number: '',
    customer_name: '',
    quantity: 1,
    weight: '',
    courier: '',
    location: '',
    shelf_number: '',
    notes: ''
  };

  // Available couriers
  const couriers = [
    'FedEx',
    'UPS',
    'USPS',
    'DHL',
    'Amazon Logistics'
  ];

  onMount(async () => {
    try {
      // Fetch available locations and recent packages
      const [locationsRes, packagesRes] = await Promise.all([
        fetch('http://localhost:8000/api/storage-locations/'),
        fetch('http://localhost:8000/api/packages/')
      ]);
      
      locations = await locationsRes.json();
      recentPackages = await packagesRes.json();
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  });

  const handleBarcodeDetected = (barcode) => {
    // Here you would typically make an API call to look up the package details
    // For now, we'll just populate the tracking number
    newPackage.tracking_number = barcode;
    showScannerModal = false;
    showAddPackageModal = true;
  };

  const handleSubmit = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/packages/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newPackage)
      });

      if (response.ok) {
        // Refresh package list
        const packagesRes = await fetch('http://localhost:8000/api/packages/');
        recentPackages = await packagesRes.json();
        
        // Reset form and close modal
        newPackage = {
          tracking_number: '',
          customer_name: '',
          quantity: 1,
          weight: '',
          courier: '',
          location: '',
          shelf_number: '',
          notes: ''
        };
        showAddPackageModal = false;
      }
    } catch (error) {
      console.error('Error saving package:', error);
    }
  };
</script>

<div class="p-8">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold text-white">Package Management</h1>
    <div class="space-x-4">
      <button
        on:click={() => showScannerModal = true}
        class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
      >
        Scan Barcode
      </button>
      <button
        on:click={() => showAddPackageModal = true}
        class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
      >
        Add Package Manually
      </button>
    </div>
  </div>

  <!-- Recent Packages Table -->
  <div class="bg-white/10 rounded-lg p-6">
    <h2 class="text-lg font-semibold text-white mb-4">Recent Packages</h2>
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-purple-800">
        <thead>
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Tracking #</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Customer</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Courier</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Location</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Status</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-purple-300 uppercase">Arrival Date</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-purple-800">
          {#each recentPackages as pkg}
            <tr class="text-purple-200">
              <td class="px-6 py-4 whitespace-nowrap">{pkg.tracking_number}</td>
              <td class="px-6 py-4 whitespace-nowrap">{pkg.customer_name}</td>
              <td class="px-6 py-4 whitespace-nowrap">{pkg.courier}</td>
              <td class="px-6 py-4 whitespace-nowrap">Shelf {pkg.shelf_number}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full 
                  {pkg.status === 'delivered' ? 'bg-green-900 text-green-200' : 
                    pkg.status === 'pending' ? 'bg-yellow-900 text-yellow-200' : 
                    'bg-purple-800 text-purple-200'}">
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

<!-- Scanner Modal -->
{#if showScannerModal}
  <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Scan Package Barcode</h2>
        <button
          on:click={() => showScannerModal = false}
          class="text-gray-500 hover:text-gray-700"
        >
          ×
        </button>
      </div>
      <BarcodeScanner onDetected={handleBarcodeDetected} />
    </div>
  </div>
{/if}

<!-- Add Package Modal -->
{#if showAddPackageModal}
  <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full mx-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-bold">Add New Package</h2>
        <button
          on:click={() => showAddPackageModal = false}
          class="text-gray-500 hover:text-gray-700"
        >
          ×
        </button>
      </div>
      
      <form on:submit|preventDefault={handleSubmit} class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Tracking Number</label>
            <input
              type="text"
              bind:value={newPackage.tracking_number}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Customer Name</label>
            <input
              type="text"
              bind:value={newPackage.customer_name}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Quantity</label>
            <input
              type="number"
              bind:value={newPackage.quantity}
              min="1"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Weight (kg)</label>
            <input
              type="number"
              step="0.1"
              bind:value={newPackage.weight}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Courier</label>
            <select
              bind:value={newPackage.courier}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option value="">Select courier...</option>
              {#each couriers as courier}
                <option value={courier}>{courier}</option>
              {/each}
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700">Shelf Number</label>
            <input
              type="text"
              bind:value={newPackage.shelf_number}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            bind:value={newPackage.notes}
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3 pt-4">
          <button
            type="button"
            on:click={() => showAddPackageModal = false}
            class="px-4 py-2 border rounded-md text-gray-700 hover:bg-gray-50"
          >
            Cancel
          </button>
          <button
            type="submit"
            class="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Save Package
          </button>
        </div>
      </form>
    </div>
  </div>
{/if}