<script>
    import { onMount } from 'svelte';
    let barcodeInput;
    let weightInput;
    let customerSelect;
    let locationSelect;
    let customers = [];
    let locations = [];
    let scanStatus = '';
  
    onMount(async () => {
      try {
        // Fetch customers and available locations
        const [customersRes, locationsRes] = await Promise.all([
          fetch('http://localhost:8000/api/customers/'),
          fetch('http://localhost:8000/api/locations/available/')
        ]);
        
        customers = await customersRes.json();
        locations = await locationsRes.json();
        
        // Focus barcode input on load
        barcodeInput?.focus();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    });
  
    async function handleScan(event) {
      event.preventDefault();
      
      try {
        const response = await fetch('http://localhost:8000/api/packages/scan_barcode/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            barcode_data: barcodeInput.value,
            weight: weightInput.value,
            customer_id: customerSelect.value,
            location_id: locationSelect.value
          })
        });
  
        if (response.ok) {
          scanStatus = 'Package scanned successfully!';
          barcodeInput.value = '';
          weightInput.value = '';
          barcodeInput.focus();
        } else {
          const error = await response.json();
          scanStatus = `Error: ${error.message}`;
        }
      } catch (error) {
        scanStatus = 'Error scanning package';
        console.error('Error:', error);
      }
    }
  </script>
  
  <div class="max-w-2xl mx-auto">
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h1 class="text-2xl font-bold text-gray-900 mb-6">Scan Package</h1>
        
        <form on:submit={handleScan} class="space-y-6">
          <div>
            <label for="barcode" class="block text-sm font-medium text-gray-700">
              Barcode
            </label>
            <input
              type="text"
              id="barcode"
              bind:this={barcodeInput}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              placeholder="Scan or enter barcode"
              required
            />
          </div>
  
          <div>
            <label for="weight" class="block text-sm font-medium text-gray-700">
              Weight (kg)
            </label>
            <input
              type="number"
              id="weight"
              bind:this={weightInput}
              step="0.01"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            />
          </div>
  
          <div>
            <label for="customer" class="block text-sm font-medium text-gray-700">
              Customer
            </label>
            <select
              id="customer"
              bind:this={customerSelect}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option value="">Select customer...</option>
              {#each customers as customer}
                <option value={customer.id}>{customer.name}</option>
              {/each}
            </select>
          </div>
  
          <div>
            <label for="location" class="block text-sm font-medium text-gray-700">
              Storage Location
            </label>
            <select
              id="location"
              bind:this={locationSelect}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
              required
            >
              <option value="">Select location...</option>
              {#each locations as location}
                <option value={location.id}>{location.location_code}</option>
              {/each}
            </select>
          </div>
  
          {#if scanStatus}
            <div class={`p-4 rounded-md ${scanStatus.includes('Error') ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
              {scanStatus}
            </div>
          {/if}
  
          <button
            type="submit"
            class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Process Package
          </button>
        </form>
      </div>
    </div>
  </div>