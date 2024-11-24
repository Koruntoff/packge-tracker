<!-- frontend/src/routes/schedule/+page.svelte -->
<script>
    import { onMount } from 'svelte';
    import { Calendar } from '@fullcalendar/core';
    import dayGridPlugin from '@fullcalendar/daygrid';
    import timeGridPlugin from '@fullcalendar/timegrid';
    import interactionPlugin from '@fullcalendar/interaction';
    import { format } from 'date-fns';
  
    let calendar;
    let calendarEl;
    let showAddModal = false;
    let newEvent = {
      title: '',
      event_type: 'exhibitor',
      start_time: '',
      end_time: '',
      description: '',
      location: ''
    };
  
    let selectedFilters = {
      exhibitor: true,
      package_delivery: true,
      package_pickup: true
    };
  
    async function loadEvents() {
      try {
        const filters = Object.entries(selectedFilters)
          .filter(([_, value]) => value)
          .map(([key]) => key)
          .join(',');
  
        const response = await fetch(
          `http://localhost:8000/api/scheduled-events/filtered/?event_type=${filters}`
        );
        const events = await response.json();
        
        return events.map(event => ({
          id: event.id,
          title: event.title,
          start: event.start_time,
          end: event.end_time,
          backgroundColor: getEventColor(event.event_type),
          extendedProps: {
            description: event.description,
            event_type: event.event_type,
            location: event.location
          }
        }));
      } catch (error) {
        console.error('Error loading events:', error);
        return [];
      }
    }
  
    function getEventColor(eventType) {
      switch(eventType) {
        case 'exhibitor':
          return '#4338ca'; // Indigo
        case 'package_delivery':
          return '#059669'; // Green
        case 'package_pickup':
          return '#dc2626'; // Red
        default:
          return '#6b7280'; // Gray
      }
    }
  
    async function handleAddEvent() {
      try {
        const response = await fetch('http://localhost:8000/api/scheduled-events/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(newEvent)
        });
  
        if (response.ok) {
          showAddModal = false;
          calendar.refetchEvents();
          newEvent = {
            title: '',
            event_type: 'exhibitor',
            start_time: '',
            end_time: '',
            description: '',
            location: ''
          };
        }
      } catch (error) {
        console.error('Error adding event:', error);
      }
    }
  
    onMount(async () => {
      const calendarEl = document.getElementById('calendar');
      calendar = new Calendar(calendarEl, {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: await loadEvents(),
        eventClick: function(info) {
          alert(`
            Event: ${info.event.title}
            Type: ${info.event.extendedProps.event_type}
            Description: ${info.event.extendedProps.description || 'No description'}
            Location: ${info.event.extendedProps.location || 'No location'}
          `);
        },
        dateClick: function(info) {
          newEvent.start_time = info.dateStr;
          showAddModal = true;
        }
      });
  
      calendar.render();
    });
  
    async function handleFilterChange() {
      const events = await loadEvents();
      calendar.removeAllEvents();
      calendar.addEventSource(events);
    }
  </script>
  
  <div class="p-8">
    <div class="mb-6 flex justify-between items-center">
      <h1 class="text-2xl font-bold text-white">Schedule</h1>
      <button
        on:click={() => showAddModal = true}
        class="bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700"
      >
        Add Event
      </button>
    </div>
  
    <!-- Filters -->
    <div class="mb-6 flex space-x-4">
      <label class="flex items-center text-white">
        <input
          type="checkbox"
          bind:checked={selectedFilters.exhibitor}
          on:change={handleFilterChange}
          class="mr-2"
        />
        Exhibitors
      </label>
      <label class="flex items-center text-white">
        <input
          type="checkbox"
          bind:checked={selectedFilters.package_delivery}
          on:change={handleFilterChange}
          class="mr-2"
        />
        Package Deliveries
      </label>
      <label class="flex items-center text-white">
        <input
          type="checkbox"
          bind:checked={selectedFilters.package_pickup}
          on:change={handleFilterChange}
          class="mr-2"
        />
        Package Pickups
      </label>
    </div>
  
    <!-- Calendar -->
    <div class="bg-white rounded-lg p-6">
      <div id="calendar"></div>
    </div>
  </div>
  
  <!-- Add Event Modal -->
  {#if showAddModal}
    <div class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 max-w-lg w-full mx-4">
        <h2 class="text-xl font-bold mb-4">Add New Event</h2>
        
        <form on:submit|preventDefault={handleAddEvent} class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              bind:value={newEvent.title}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Event Type</label>
            <select
              bind:value={newEvent.event_type}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              required
            >
              <option value="exhibitor">Exhibitor</option>
              <option value="package_delivery">Package Delivery</option>
              <option value="package_pickup">Package Pickup</option>
            </select>
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Start Time</label>
            <input
              type="datetime-local"
              bind:value={newEvent.start_time}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">End Time</label>
            <input
              type="datetime-local"
              bind:value={newEvent.end_time}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Location</label>
            <input
              type="text"
              bind:value={newEvent.location}
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              bind:value={newEvent.description}
              rows="3"
              class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-purple-500 focus:ring-purple-500"
            ></textarea>
          </div>
  
          <div class="flex justify-end space-x-3 pt-4">
            <button
              type="button"
              on:click={() => showAddModal = false}
              class="px-4 py-2 border rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
            >
              Add Event
            </button>
          </div>
        </form>
      </div>
    </div>
  {/if}
  
  <style>
    :global(.fc) {
      /* FullCalendar styles */
      background-color: white;
      padding: 1rem;
      border-radius: 0.5rem;
    }
    
    :global(.fc-event) {
      cursor: pointer;
    }
  </style>