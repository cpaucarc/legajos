function cerrarBlock(){
  $.blockUI({
      message: '<i style="font-size:36px;" class="fa fa-spinner fa-pulse fa-fw"></i>',
      timeout: 1,
      overlayCSS: {
          backgroundColor: '#000',
          opacity: 0.5,
          cursor: 'wait'
      },
      css: {
          border: 0,
          padding: 0,
          color: '#333',
          backgroundColor: 'transparent'
      }
  });
}

function cargarBlock(){
  $.blockUI({
      message: '<i style="font-size:36px;" class="fa fa-spinner fa-pulse fa-fw"></i>',
      timeout: 1000000,
      overlayCSS: {
          backgroundColor: '#000',
          opacity: 0.5,
          cursor: 'wait'
      },
      css: {
          border: 0,
          padding: 0,
          backgroundColor: 'transparent'
      }
  });
}