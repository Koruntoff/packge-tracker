<script>
  import { onMount } from 'svelte';
  import BarcodeScanner from '../../lib/components/BarcodeScanner.svelte';
  
  let showScannerModal = false;
  let scanning = false;
  let scanStatus = ''; // For showing feedback messages
  let recentPackages = [];
  let locations = [];
  
  // New package form data with default values
  let newPackage = {
    tracking_number: '',
    customer_name: '',
    quantity: 1,
    weight: '',
    courier: '',
    location: '',
    shelf_number: '',
    notes: '',
    status: 'received' // Default status
  };

  const couriers = ['FedEx', 'UPS', 'USPS', 'DHL', 'Amazon'];

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

  // First, try to find an existing package
  const findExistingPackage = async (barcode) => {
    try {
      const response = await fetch(`http://localhost:8000/api/packages/?tracking_number=${barcode}`);
      const packages = await response.json();
      return packages.length > 0 ? packages[0] : null;
    } catch (error) {
      console.error('Error finding package:', error);
      return null;
    }
  };

  // Try to find customer by tracking number pattern
  const findCustomer = async (trackingNumber) => {
    try {
      // You might want to implement this endpoint in your backend
      const response = await fetch(`http://localhost:8000/api/customers/find-by-tracking/?number=${trackingNumber}`);
      if (response.ok) {
        return await response.json();
      }
      return null;
    } catch (error) {
      console.error('Error finding customer:', error);
      return null;
    }
  };

  // Find available storage location
  const findAvailableLocation = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/storage-locations/available/');
      if (response.ok) {
        const availableLocations = await response.json();
        return availableLocations.length > 0 ? availableLocations[0] : null;
      }
      return null;
    } catch (error) {
      console.error('Error finding location:', error);
      return null;
    }
  };

  // Determine courier from tracking number pattern
  const determineCourier = (trackingNumber) => {
    // Add your courier detection logic here
    if (trackingNumber.startsWith('1Z')) return 'UPS';
    if (trackingNumber.match(/\b(94|93|92|94|95)[0-9]{20}\b/)) return 'USPS';
    if (trackingNumber.match(/\b([0-9]{12}|[0-9]{15})\b/)) return 'FedEx';
    if (trackingNumber.match(/\b([0-9]{10})\b/)) return 'DHL';
    if (trackingNumber.startsWith('TBA')) return 'Amazon';
    return '';
  };

  const handleBarcodeDetected = async (barcode) => {
    try {
      scanStatus = 'Processing barcode...';
      showScannerModal = false;
      
      // Check if package already exists
      const existingPackage = await findExistingPackage(barcode);
      if (existingPackage) {
        scanStatus = 'Package already in system!';
        return;
      }

      // Start building the new package
      newPackage.tracking_number = barcode;
      newPackage.courier = determineCourier(barcode);
      
      // Try to find customer
      const customer = await findCustomer(barcode);
      if (customer) {
        newPackage.customer_name = customer.name;
      }
      
      // Find available storage location
      const location = await findAvailableLocation();
      if (location) {
        newPackage.location = location.id;
        newPackage.shelf_number = location.shelf_number;
      }

      // If we have all required fields, automatically save
      if (newPackage.customer_name && newPackage.location) {
        await handleSubmit();
        scanStatus = 'Package automatically processed!';
      } else {
        // If we're missing some info, show the form
        showAddPackageModal = true;
        scanStatus = 'Please complete missing information.';
      }
    } catch (error) {
      console.error('Error processing barcode:', error);
      scanStatus = 'Error processing barcode. Please try again.';
    }
  };

  const handleSubmit = async () => {
    try {
      scanStatus = 'Saving package...';
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
        
        // Reset form
        newPackage = {
          tracking_number: '',
          customer_name: '',
          quantity: 1,
          weight: '',
          courier: '',
          location: '',
          shelf_number: '',
          notes: '',
          status: 'received'
        };
        showAddPackageModal = false;
        scanStatus = 'Package saved successfully!';
      } else {
        scanStatus = 'Error saving package.';
      }
    } catch (error) {
      console.error('Error saving package:', error);
      scanStatus = 'Error saving package.';
    }
  };
</script>

<!-- Rest of your template remains the same, but add status message display -->
<div class="p-8">
  <!-- Status Message -->
  {#if scanStatus}
    <div class="mb-4 p-4 rounded-md {scanStatus.includes('Error') ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}">
      {scanStatus}
    </div>
  {/if}

  <!-- Rest of your existing template... -->
</div>