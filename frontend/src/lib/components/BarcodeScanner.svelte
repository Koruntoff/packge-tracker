<script>
    import { onMount, onDestroy } from 'svelte';
    import Quagga from 'quagga';
  
    export let onDetected = (result) => {};
    let scannerElement;
  
    onMount(() => {
      if (scannerElement) {
        Quagga.init({
          inputStream: {
            name: "Live",
            type: "LiveStream",
            target: scannerElement,
            constraints: {
              facingMode: "environment"
            },
          },
          decoder: {
            readers: [
              "ean_reader",
              "ean_8_reader",
              "code_128_reader",
              "code_39_reader",
              "upc_reader"
            ]
          }
        }, (err) => {
          if (err) {
            console.error(err);
            return;
          }
          Quagga.start();
        });
  
        Quagga.onDetected((result) => {
          const code = result.codeResult.code;
          onDetected(code);
        });
      }
    });
  
    onDestroy(() => {
      Quagga.stop();
    });
  </script>
  
  <div bind:this={scannerElement} class="w-full h-64 relative">
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="w-64 h-1 bg-red-500 opacity-50"></div>
    </div>
    <div class="absolute inset-0 flex items-center justify-center">
      <div class="w-1 h-64 bg-red-500 opacity-50"></div>
    </div>
  </div>